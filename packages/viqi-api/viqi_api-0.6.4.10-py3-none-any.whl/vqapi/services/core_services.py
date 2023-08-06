# import functools
import logging
import pickle
import posixpath
import shutil
import tempfile

import requests
from bq.metadoc.formats import Metadoc

from vqapi.exception import BQApiError, code_to_exception
from vqapi.util import is_uniq_code

# from botocore.credentials import RefreshableCredentials
# from botocore.session import get_session

from .base_proxy import ResponseFile, ResponseFolder, BaseServiceProxy, FuturizedServiceProxy


log = logging.getLogger("vqapi.services")


################### Helpers ######################


def _prepare_mountpath(path: str) -> str:
    if path.startswith("store:"):
        path = path[len("store:") :]
    return path.strip("/")


def _prepare_uniq(id: str) -> str:
    if not is_uniq_code(id):
        raise BQApiError(f'"{id}" is not a valid resource id')
    return id


def _prepare_uniq_or_alias_or_path(id: str) -> str:
    if id.startswith("store:"):
        id = id[len("store:") :]
    return id.strip("/")



class AdminProxy(FuturizedServiceProxy):
    service_name = "admin"

    def login_as(self, user_name):
        data = self.session.service("meta")
        userxml = data.fetch("user", params={"name": user_name, "wpublic": 1}, render="doc")
        user_uniq = userxml.find(f"user[@name='{user_name}']")
        if user_uniq is not None:
            user_uniq = user_uniq.get("resource_uniq")
            response = self.fetch(f"user/{user_uniq}/login")
            response.raise_for_status()

            # check the login succeded
            user_session = self.session.service("auth_service").get("session", render="doc")
            user_id = user_session.find("user").get("value")
            # user_id is /<user_uniq"
            if user_id[1:] == user_uniq:
                return user_uniq

        # login failed
        return None

    def login_create(self, login_id: str) -> Metadoc:
        """Login as LOGIN_ID , create user if not already create

        Args:
          login_id should be a valid login id (email)
        Returns:
         a Response
        """
        resp =  self.post(f"user/{login_id}/login?create=true")
        code_to_exception(resp)
        return resp.doc()

    def fetch_user(self, login_id: str):
        resp = self.get(f"user/{login_id}")
        code_to_exception(resp)
        return resp.doc()

    def delete_user(self, login_id: str):
        resp = self.delete(f"user/{login_id}")
        code_to_exception(resp)


class AuthProxy(FuturizedServiceProxy):
    service_name = "auths"
    def login_providers(self, **kw):
        return self.request("login_providers", **kw)

    def credentials(self, **kw):
        return self.request("credentials", **kw)

    def get_session(self, **kw):  # hides session
        return self.request("session", **kw)

    def get(self, path=None, params=None, render=None, **kw):
        res = super().get(path=path, params=params, render=render, **kw)
        return self._prep_result(res, render)


class BlobProxy(FuturizedServiceProxy):
    service_name = "blobs"

    def create_blob(self, path: str, blob: object):
        """Create binary resource at given path from the given object/file.

        Args:
            path (str): mountpath for new blob
            blob (object): object to store (if str, is assumed to be local filename)

        Raises:
            DuplicateFile: path already exists
            ResourceNotFoundError: path not valid
            IllegalOperation: blob creation not allowed at given path
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.create_blob('store://mymount/my/path/name.jpg', '/tmp/image.jpg')
        """
        # prep inputs
        path = _prepare_mountpath(path)
        if not isinstance(blob, str):
            filedata = pickle.dumps(blob)

        try:
            filedata = open(blob, "rb")
            res = self.post(path, headers={"Content-Type": "application/octet-stream"}, data=filedata)
            # prep outputs
            code_to_exception(res)
        finally:
            if hasattr(filedata, "close"):
                filedata.close()

    def delete_blob(self, path: str):
        """Delete binary resource at given path.

        Args:
            path (str): mountpath for blob to delete

        Raises:
            ResourceNotFoundError: path not valid
            IllegalOperation: blob deletion not allowed (e.g., resource is registered or path is container)
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.delete_blob('store://mymount/my/path/name.jpg')
        """
        # prep inputs
        path = _prepare_mountpath(path)

        res = self.delete(path)

        # prep outputs
        code_to_exception(res)

    def register(self, path: str = None, resource: Metadoc = None) -> Metadoc:
        """Register blob at a given mount path.

        Args:
            path (str, optional): mountpath to blob
            resource (Metadoc, optional): assign suggested type, permissions and metadata at registration time

        Returns:
            Metadoc: resource document

        Raises:
            AlreadyRegisteredError: blob already registered
            ResourceNotFoundError: path not valid
            IllegalOperation: blob registration not allowed at given path
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.register(path='store://mymount/my/path/name.jpg')
            <Metadoc at 0x...>
        """
        # prep inputs
        log.debug(f"register {path}")
        path = _prepare_mountpath(path)

        res = self.post(posixpath.join("register", path), data=resource)

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def unregister(self, path: str = None, resource: Metadoc = None):
        """Unregister blob with given id.

        Args:
            path (str, optional): mount-path of blob
            resource (Metadoc, optional): resource to unregister

        Returns:
            bool: True, if successfully unregistered

        Raises:
            ResourceNotFoundError: invalid mount-path or id
            NotRegisteredError: blob not registered

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> blob_service.unregister(path='store://mymount/my/path/name.jpg')
            True
        """
        # prep inputs
        log.debug(f"unregister {path}")
        if path is None and resource is not None:
            path = resource.text.split(",", 1)[0]
        log.debug(f"unregister {path}")
        path = _prepare_mountpath(path)

        res = self.post(posixpath.join("unregister", path))

        # prep outputs
        code_to_exception(res)

        return True

    def read_chunk(
        self,
        blob_id: str,
        content_selector: str = None,
        vts: str = None,
        as_stream: bool = False,
    ):
        """Read chunk of resource specified by id.

        Args:
            blob_id (uuid): mount-path or uuid or alias of blob
            content_selector (str): blob-specific selector of subset to return (or all if None)
            vts (str): version timestamp to return (or latest if None)
            as_stream (bool): return chunk as bytes stream (ResponseFile/ResponseFolder), otherwise return as localpath

        Returns:
            ResponseFile or ResponseFolder or bytes: file obj or folder obj or blob byte array

        Raises:
            NoAuthorizationError: no access permission for blob
            ResourceNotFoundError: no blob with given id
            BQApiError: any other error

        Examples:
            >>> blob_service = bqsession.service('blobs')
            >>> with blob_service.read_chunk('00-123456789', as_stream=True) as fp:
            >>>    fo.read(1024)
        """
        # prep inputs
        blob_id = _prepare_uniq_or_alias_or_path(blob_id)

        headers = {}
        if content_selector is not None:
            headers["x-content-selector"] = content_selector
        if vts is not None:
            headers["x-vts"] = vts
        res = self.get(f"/{blob_id}", headers=headers, stream=as_stream)

        # prep outputs
        code_to_exception(res)

        if res.headers["content-type"] == "application/x-tar":
            # this is a tarfile of a folder structure
            res = ResponseFolder(res)
        else:
            # this is a single file
            res = ResponseFile(res)

        if as_stream:
            return res
        else:
            # caller wants local copy... this may be never used/needed...
            localpath = tempfile.mkdtemp()  # who deletes this?
            return res.copy_into(localpath)



class DatasetProxy(FuturizedServiceProxy):
    service_name = "datasets"

    def create(self, dataset_name, member_list, **kw):
        """Create a dataset from a list of resource_uniq elements"""
        data = self.session.service("data_service")
        dataset = Metadoc(tag="dataset", name=dataset_name)
        for member_uniq in member_list:
            member = dataset.add_tag("value", type="object")
            member.text = member_uniq

        return data.post(data=dataset, render="doc")
    def append_member(self, dataset_uniq, resource_uniq, **kw):
        """Append an objects to dataset
        Args:
           resource_uniq: str or list
        """
        data = self.session.service("data_service")
        patch = Metadoc(tag="patch")
        if isinstance(resource_uniq, str):
            resource_uniq = [ resource_uniq ]
        for uniq in resource_uniq:
            member = Metadoc(tag="value", type="object", value=uniq)
            patch.add_tag(tag="add", sel=f"/{dataset_uniq}").add_child(member)
        data.patch(data=patch)

    def delete(self, dataset_uniq, members=False, **kw):
        data = self.session.service("data_service")
        if not members:
            data.delete(path=f"{dataset_uniq}")
            return
        dataset = data.fetch(docid=f"/{dataset_uniq}", view="deep")
        patch = Metadoc(tag="patch")
        for uniq in list(members):
            uris = dataset.path_query(f"value[@value='{uniq}']/@uri")
            for uri in uris:
                patch.add_tag(tag="remove", sel="/{uri}")
        data.patch(data=patch)

    def delete_member(self, dataset_uniq, resource_uniq, **kw):
        """Delete a member..
        @return new dataset if success or None
        """
        raise NotImplementedError
        # data = self.session.service("data_service")
        # dataset = data.fetch(dataset_uniq, params={"view": "full"}, render="doc")
        # members = dataset.path_query('value[text()="%s"]' % data.construct(resource_uniq))
        # for member in members:
        #     member.delete()
        # if len(members):
        #     return data.put(dataset_uniq, data=dataset, render="doc")
        # return None


class MexProxy(FuturizedServiceProxy):
    service_name = "mexes"

    def get_all_mexes(self) -> Metadoc:
        """Get module execution (mex) documents for all running modules.

        Returns:
            Metadoc: mex document

        Raises:
            BQApiError: any other error

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_all_mexes()
            <Metadoc at 0x...>
        """
        res = self.get("")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def get_mex(self, mex_id: str) -> Metadoc:
        """Get module execution (mex) document for the execution specified.

        Args:
            mex_id (uuid): mex uniq

        Returns:
            Metadoc: mex document

        Raises:
            MexNotFoundError: if no mex with given id was found
            BQApiError: any other error

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_mex('00-123456789')
            <Metadoc at 0x...>
        """
        # prep inputs
        mex_id = _prepare_uniq(mex_id)

        res = self.get(f"/{mex_id}")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def get_mex_log(self, mex_id: str) -> Metadoc:
        """Get module execution (mex) log for the execution specified.

        Args:
            mex_id (uuid): execution identifier

        Returns:
            Metadoc: <log>logtext</log>

        Raises:
            MexNotFoundError: if no mex with given id was found

        Examples:
            >>> mex_service = bqsession.service('mexes')
            >>> mex_service.get_mex_log('00-123456789')
            2021-07-02 03:00:56,848 DEBUG [urllib3.connectionpool] (_new_conn) - Starting ne...
        """
        # prep inputs
        mex_id = _prepare_uniq(mex_id)

        res = self.get(f"/{mex_id}/log")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def request(self, path=None, params=None, method="get", render=None, **kw):
        # TODO: add real api fct
        res = super().request(path=path, params=params, method=method, render=render, **kw)
        return self._prep_result(res, render)



class ExportProxy(FuturizedServiceProxy):

    ## service_name = "export"  # NOT Implemented

    valid_param = {"files", "datasets", "dirs", "urls", "users", "compression"}

    def fetch_export(self, **kw):
        params = {key: val for key, val in list(kw.items()) if key in self.valid_param and val is not None}
        response = self.fetch("stream", params=params, stream=kw.pop("stream", True))
        return response

    def fetch_export_local(self, localpath, stream=True, **kw):
        response = self.fetch_export(stream=stream, **kw)
        if response.status_code == requests.codes.ok:
            with open(localpath, "wb") as f:
                shutil.copyfileobj(response.raw, f)
        return response


class DataProxy(FuturizedServiceProxy):
    service_name = "meta"

    # TODO: add real API fcts
    def request(self, path=None, params=None, method="get", render="doc", view=None, **kw):
        if view is not None:
            if isinstance(view, list):
                view = ",".join(view)
            params = params or {}
            params["view"] = view

        res = super().request(path=path, params=params, method=method, render=render, **kw)

        # prep outputs
        code_to_exception(res)

        return self._prep_result(res, render)

    def fetch(self, path=None, params=None, render="doc", **kw):
        return super().fetch(path=path, params=params, render=render, **kw)

    def get(self, path=None, params=None, render="doc", **kw):
        return super().get(path=path, params=params, render=render, **kw)

    def patch(self, path=None, params=None, render="doc", **kw):
        return super().patch(path=path, params=params, render=render, **kw)

    def post(self, path=None, params=None, render="doc", **kw):
        return super().post(path=path, params=params, render=render, **kw)

    def put(self, path=None, params=None, render="doc", **kw):
        return super().put(path=path, params=params, render=render, **kw)

    def delete(self, path=None, params=None, render=None, **kw):
        return super().delete(path=path, params=params, render=render, **kw)


class DirProxy(FuturizedServiceProxy):
    service_name = "dirs"

    def create_container(self, path: str, name: str, container_type: str = "folder"):
        """Create new container with name at given path.

        Args:
            path (str): mountpath holding new container
            name (str): name of new container
            container_type (str): 'folder' or 'tablecontainer'

        Raises:
            IllegalOperation: path already exists
            ResourceNotFoundError: path not valid

        Examples:
            >>> dir_service = bqsession.service('dirs')
            >>> dir_service.create_container('store://mymount/my/path', 'new_container', container_type='tablecontainer')
        """
        # prep inputs
        path = _prepare_mountpath(path)

        res = self.post(
            path,
            data=Metadoc.from_naturalxml(f'<dir name="{name}" type="{container_type}" />'),
        )

        # prep outputs
        code_to_exception(res)

    def list_files(
        self,
        path,
        want_meta=False,
        want_types=False,
        patterns=None,
        limit=100,
        offset=0,
    ):
        """List all entries (registered and unregistered, resources and containers) at the given path.

        Args:
            path (str): mount-path to list
            want_meta (bool): if True, include metadata per entry
            want_types (bool): if True, include type guesses per entry (slow!)
            patterns (list of str): one or more wildcard patterns for filtering of entries (these are ORed)
            limit (int): max number of entries to return
            offset (int): starting entry number (for paging)

        Returns:
            Metadoc: doc describing path and all selected entries as children

        Raises:
            NoSuchFileError: file at mount-path does not exist
            NoSuchPathError: mount-path does not exist
            IllegalOperation: mount does not exist

        Examples:
            >>> dir_service = bqsession.service('dirs')
            >>> str(dir_service.list_files('/mymount/dir1', limit=10))
            '<dir name="mymount" ...> <dir ... /> ... <image ... /> <resource ... /> </dir>'
        """
        # prep inputs
        params = {}
        view_options = []
        if want_meta:
            view_options.append("meta")
        if want_types:
            view_options.append("types")
        if view_options:
            params["view"] = ",".join(view_options)
        if patterns:
            params["patterns"] = ",".join(patterns)
        params["limit"] = limit
        params["offset"] = offset

        res = self.get(path, params=params)

        # prep outputs
        code_to_exception(res)

        return res.doc()


class FutureProxy(FuturizedServiceProxy):
    service_name = "futures"

    def get_state(self, future_id):
        """Get state of the future with the given id.

        Args:
            future_id: future id

        Returns:
            str: state of future (e.g., PENDING or FINISHED)

        Raises:
            FutureNotFoundError: if no future with given id was found
            BQApiError: any other error

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.get_state('8196770f-ea2e-4bc6-b569-9e29fc031d46')
            'PENDING'
        """
        res = self.get(f"/{future_id}")

        # prep outputs
        code_to_exception(res)

        return res.doc().get("state")

    def get_result(self, future_id):
        """Get result of the future with the given id.

        Args:
            future_id: future id

        Returns:
            Metadoc: result of the future or None, if no result

        Raises:
            ValueError: result can not be rendered as doc
            FutureNotFoundError: if no future with given id was found
            FutureNotReadyError: if future result is not ready yet
            BQApiError: any other error
            Exception: any exception raised by the async task

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.get_result('8196770f-ea2e-4bc6-b569-9e29fc031d46')
            <Metadoc at 0x...>
        """
        res = self.get(f"/{future_id}/result")

        # prep outputs
        code_to_exception(res)

        return res.doc()

    def delete(self, future_id):
        """Delete future with the given id.

        Args:
            future_id: future id

        Raises:
            FutureNotFoundError: if no future with given id was found
            BQApiError: any other error

        Examples:
            >>> future_service = bqsession.service('futures')
            >>> future_service.delete('8196770f-ea2e-4bc6-b569-9e29fc031d46')
        """
        res = super().delete(f"/{future_id}")

        # prep outputs
        code_to_exception(res)

class ServicesProxy(BaseServiceProxy):
    service_name = "services"


def test_module():
    from vqapi import VQSession

    session = VQSession().init_local("admin", "admin", "http://localhost:8080")
    admin = session.service("admin")
    data = session.service("data_service")
    # admin.user(uniq).login().fetch ()
    xml = data.get("user", params={"resource_name": "admin"}, render="doc")
    user_uniq = xml.find("user").get("resource_uniq")
    admin.fetch(f"/user/{user_uniq}/login")


if __name__ == "__main__":
    test_module()
