# Python stubs generated by omniidl from /home/openrtm/svn/OpenRTM-aist-Python/OpenRTM_aist/RTM_IDL/Manager.idl

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA

_omnipy.checkVersion(3,0, __file__)

# #include "SDOPackage.idl"
import SDOPackage_idl
_0_SDOPackage = omniORB.openModule("SDOPackage")
_0_SDOPackage__POA = omniORB.openModule("SDOPackage__POA")
# #include "RTC.idl"
import RTC_idl
_0_RTC = omniORB.openModule("RTC")
_0_RTC__POA = omniORB.openModule("RTC__POA")

#
# Start of module "RTM"
#
__name__ = "RTM"
_0_RTM = omniORB.openModule("RTM", r"/home/openrtm/svn/OpenRTM-aist-Python/OpenRTM_aist/RTM_IDL/Manager.idl")
_0_RTM__POA = omniORB.openModule("RTM__POA", r"/home/openrtm/svn/OpenRTM-aist-Python/OpenRTM_aist/RTM_IDL/Manager.idl")


# typedef ... NVList
class NVList:
    _NP_RepositoryId = "IDL:RTM/NVList:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_RTM.NVList = NVList
_0_RTM._d_NVList  = omniORB.typeMapping["IDL:org.omg/SDOPackage/NVList:1.0"]
_0_RTM._ad_NVList = (omniORB.tcInternal.tv_alias, NVList._NP_RepositoryId, "NVList", omniORB.typeCodeMapping["IDL:org.omg/SDOPackage/NVList:1.0"]._d)
_0_RTM._tc_NVList = omniORB.tcInternal.createTypeCode(_0_RTM._ad_NVList)
omniORB.registerType(NVList._NP_RepositoryId, _0_RTM._ad_NVList, _0_RTM._tc_NVList)
del NVList

# struct ModuleProfile
_0_RTM.ModuleProfile = omniORB.newEmptyClass()
class ModuleProfile (omniORB.StructBase):
    _NP_RepositoryId = "IDL:RTM/ModuleProfile:1.0"

    def __init__(self, properties):
        self.properties = properties

_0_RTM.ModuleProfile = ModuleProfile
_0_RTM._d_ModuleProfile  = (omniORB.tcInternal.tv_struct, ModuleProfile, ModuleProfile._NP_RepositoryId, "ModuleProfile", "properties", omniORB.typeMapping["IDL:RTM/NVList:1.0"])
_0_RTM._tc_ModuleProfile = omniORB.tcInternal.createTypeCode(_0_RTM._d_ModuleProfile)
omniORB.registerType(ModuleProfile._NP_RepositoryId, _0_RTM._d_ModuleProfile, _0_RTM._tc_ModuleProfile)
del ModuleProfile

# typedef ... ModuleProfileList
class ModuleProfileList:
    _NP_RepositoryId = "IDL:RTM/ModuleProfileList:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_RTM.ModuleProfileList = ModuleProfileList
_0_RTM._d_ModuleProfileList  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:RTM/ModuleProfile:1.0"], 0)
_0_RTM._ad_ModuleProfileList = (omniORB.tcInternal.tv_alias, ModuleProfileList._NP_RepositoryId, "ModuleProfileList", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:RTM/ModuleProfile:1.0"], 0))
_0_RTM._tc_ModuleProfileList = omniORB.tcInternal.createTypeCode(_0_RTM._ad_ModuleProfileList)
omniORB.registerType(ModuleProfileList._NP_RepositoryId, _0_RTM._ad_ModuleProfileList, _0_RTM._tc_ModuleProfileList)
del ModuleProfileList

# struct ManagerProfile
_0_RTM.ManagerProfile = omniORB.newEmptyClass()
class ManagerProfile (omniORB.StructBase):
    _NP_RepositoryId = "IDL:RTM/ManagerProfile:1.0"

    def __init__(self, properties):
        self.properties = properties

_0_RTM.ManagerProfile = ManagerProfile
_0_RTM._d_ManagerProfile  = (omniORB.tcInternal.tv_struct, ManagerProfile, ManagerProfile._NP_RepositoryId, "ManagerProfile", "properties", omniORB.typeMapping["IDL:RTM/NVList:1.0"])
_0_RTM._tc_ManagerProfile = omniORB.tcInternal.createTypeCode(_0_RTM._d_ManagerProfile)
omniORB.registerType(ManagerProfile._NP_RepositoryId, _0_RTM._d_ManagerProfile, _0_RTM._tc_ManagerProfile)
del ManagerProfile

# interface Manager;
_0_RTM._d_Manager = (omniORB.tcInternal.tv_objref, "IDL:RTM/Manager:1.0", "Manager")
omniORB.typeMapping["IDL:RTM/Manager:1.0"] = _0_RTM._d_Manager

# typedef ... ManagerList
class ManagerList:
    _NP_RepositoryId = "IDL:RTM/ManagerList:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_RTM.ManagerList = ManagerList
_0_RTM._d_ManagerList  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:RTM/Manager:1.0"], 0)
_0_RTM._ad_ManagerList = (omniORB.tcInternal.tv_alias, ManagerList._NP_RepositoryId, "ManagerList", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:RTM/Manager:1.0"], 0))
_0_RTM._tc_ManagerList = omniORB.tcInternal.createTypeCode(_0_RTM._ad_ManagerList)
omniORB.registerType(ManagerList._NP_RepositoryId, _0_RTM._ad_ManagerList, _0_RTM._tc_ManagerList)
del ManagerList

# interface Manager
_0_RTM._d_Manager = (omniORB.tcInternal.tv_objref, "IDL:RTM/Manager:1.0", "Manager")
omniORB.typeMapping["IDL:RTM/Manager:1.0"] = _0_RTM._d_Manager
_0_RTM.Manager = omniORB.newEmptyClass()
class Manager :
    _NP_RepositoryId = _0_RTM._d_Manager[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_RTM.Manager = Manager
_0_RTM._tc_Manager = omniORB.tcInternal.createTypeCode(_0_RTM._d_Manager)
omniORB.registerType(Manager._NP_RepositoryId, _0_RTM._d_Manager, _0_RTM._tc_Manager)

# Manager operations and attributes
Manager._d_load_module = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_unload_module = (((omniORB.tcInternal.tv_string,0), ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_get_loadable_modules = ((), (omniORB.typeMapping["IDL:RTM/ModuleProfileList:1.0"], ), None)
Manager._d_get_loaded_modules = ((), (omniORB.typeMapping["IDL:RTM/ModuleProfileList:1.0"], ), None)
Manager._d_get_factory_profiles = ((), (omniORB.typeMapping["IDL:RTM/ModuleProfileList:1.0"], ), None)
Manager._d_create_component = (((omniORB.tcInternal.tv_string,0), ), (omniORB.typeMapping["IDL:omg.org/RTC/RTObject:1.0"], ), None)
Manager._d_delete_component = (((omniORB.tcInternal.tv_string,0), ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_get_components = ((), (omniORB.typeMapping["IDL:omg.org/RTC/RTCList:1.0"], ), None)
Manager._d_get_component_profiles = ((), (omniORB.typeMapping["IDL:omg.org/RTC/ComponentProfileList:1.0"], ), None)
Manager._d_get_profile = ((), (omniORB.typeMapping["IDL:RTM/ManagerProfile:1.0"], ), None)
Manager._d_get_configuration = ((), (omniORB.typeMapping["IDL:RTM/NVList:1.0"], ), None)
Manager._d_set_configuration = (((omniORB.tcInternal.tv_string,0), (omniORB.tcInternal.tv_string,0)), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_is_master = ((), (omniORB.tcInternal.tv_boolean, ), None)
Manager._d_get_master_managers = ((), (omniORB.typeMapping["IDL:RTM/ManagerList:1.0"], ), None)
Manager._d_add_master_manager = ((omniORB.typeMapping["IDL:RTM/Manager:1.0"], ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_remove_master_manager = ((omniORB.typeMapping["IDL:RTM/Manager:1.0"], ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_get_slave_managers = ((), (omniORB.typeMapping["IDL:RTM/ManagerList:1.0"], ), None)
Manager._d_add_slave_manager = ((omniORB.typeMapping["IDL:RTM/Manager:1.0"], ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_remove_slave_manager = ((omniORB.typeMapping["IDL:RTM/Manager:1.0"], ), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_fork = ((), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_shutdown = ((), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_restart = ((), (omniORB.typeMapping["IDL:omg.org/RTC/ReturnCode_t:1.0"], ), None)
Manager._d_get_service = (((omniORB.tcInternal.tv_string,0), ), (omniORB.typeMapping["IDL:omg.org/CORBA/Object:1.0"], ), None)

# Manager object reference
class _objref_Manager (CORBA.Object):
    _NP_RepositoryId = Manager._NP_RepositoryId

    def __init__(self):
        CORBA.Object.__init__(self)

    def load_module(self, *args):
        return _omnipy.invoke(self, "load_module", _0_RTM.Manager._d_load_module, args)

    def unload_module(self, *args):
        return _omnipy.invoke(self, "unload_module", _0_RTM.Manager._d_unload_module, args)

    def get_loadable_modules(self, *args):
        return _omnipy.invoke(self, "get_loadable_modules", _0_RTM.Manager._d_get_loadable_modules, args)

    def get_loaded_modules(self, *args):
        return _omnipy.invoke(self, "get_loaded_modules", _0_RTM.Manager._d_get_loaded_modules, args)

    def get_factory_profiles(self, *args):
        return _omnipy.invoke(self, "get_factory_profiles", _0_RTM.Manager._d_get_factory_profiles, args)

    def create_component(self, *args):
        return _omnipy.invoke(self, "create_component", _0_RTM.Manager._d_create_component, args)

    def delete_component(self, *args):
        return _omnipy.invoke(self, "delete_component", _0_RTM.Manager._d_delete_component, args)

    def get_components(self, *args):
        return _omnipy.invoke(self, "get_components", _0_RTM.Manager._d_get_components, args)

    def get_component_profiles(self, *args):
        return _omnipy.invoke(self, "get_component_profiles", _0_RTM.Manager._d_get_component_profiles, args)

    def get_profile(self, *args):
        return _omnipy.invoke(self, "get_profile", _0_RTM.Manager._d_get_profile, args)

    def get_configuration(self, *args):
        return _omnipy.invoke(self, "get_configuration", _0_RTM.Manager._d_get_configuration, args)

    def set_configuration(self, *args):
        return _omnipy.invoke(self, "set_configuration", _0_RTM.Manager._d_set_configuration, args)

    def is_master(self, *args):
        return _omnipy.invoke(self, "is_master", _0_RTM.Manager._d_is_master, args)

    def get_master_managers(self, *args):
        return _omnipy.invoke(self, "get_master_managers", _0_RTM.Manager._d_get_master_managers, args)

    def add_master_manager(self, *args):
        return _omnipy.invoke(self, "add_master_manager", _0_RTM.Manager._d_add_master_manager, args)

    def remove_master_manager(self, *args):
        return _omnipy.invoke(self, "remove_master_manager", _0_RTM.Manager._d_remove_master_manager, args)

    def get_slave_managers(self, *args):
        return _omnipy.invoke(self, "get_slave_managers", _0_RTM.Manager._d_get_slave_managers, args)

    def add_slave_manager(self, *args):
        return _omnipy.invoke(self, "add_slave_manager", _0_RTM.Manager._d_add_slave_manager, args)

    def remove_slave_manager(self, *args):
        return _omnipy.invoke(self, "remove_slave_manager", _0_RTM.Manager._d_remove_slave_manager, args)

    def fork(self, *args):
        return _omnipy.invoke(self, "fork", _0_RTM.Manager._d_fork, args)

    def shutdown(self, *args):
        return _omnipy.invoke(self, "shutdown", _0_RTM.Manager._d_shutdown, args)

    def restart(self, *args):
        return _omnipy.invoke(self, "restart", _0_RTM.Manager._d_restart, args)

    def get_service(self, *args):
        return _omnipy.invoke(self, "get_service", _0_RTM.Manager._d_get_service, args)

    __methods__ = ["load_module", "unload_module", "get_loadable_modules", "get_loaded_modules", "get_factory_profiles", "create_component", "delete_component", "get_components", "get_component_profiles", "get_profile", "get_configuration", "set_configuration", "is_master", "get_master_managers", "add_master_manager", "remove_master_manager", "get_slave_managers", "add_slave_manager", "remove_slave_manager", "fork", "shutdown", "restart", "get_service"] + CORBA.Object.__methods__

omniORB.registerObjref(Manager._NP_RepositoryId, _objref_Manager)
_0_RTM._objref_Manager = _objref_Manager
del Manager, _objref_Manager

# Manager skeleton
__name__ = "RTM__POA"
class Manager (PortableServer.Servant):
    _NP_RepositoryId = _0_RTM.Manager._NP_RepositoryId


    _omni_op_d = {"load_module": _0_RTM.Manager._d_load_module, "unload_module": _0_RTM.Manager._d_unload_module, "get_loadable_modules": _0_RTM.Manager._d_get_loadable_modules, "get_loaded_modules": _0_RTM.Manager._d_get_loaded_modules, "get_factory_profiles": _0_RTM.Manager._d_get_factory_profiles, "create_component": _0_RTM.Manager._d_create_component, "delete_component": _0_RTM.Manager._d_delete_component, "get_components": _0_RTM.Manager._d_get_components, "get_component_profiles": _0_RTM.Manager._d_get_component_profiles, "get_profile": _0_RTM.Manager._d_get_profile, "get_configuration": _0_RTM.Manager._d_get_configuration, "set_configuration": _0_RTM.Manager._d_set_configuration, "is_master": _0_RTM.Manager._d_is_master, "get_master_managers": _0_RTM.Manager._d_get_master_managers, "add_master_manager": _0_RTM.Manager._d_add_master_manager, "remove_master_manager": _0_RTM.Manager._d_remove_master_manager, "get_slave_managers": _0_RTM.Manager._d_get_slave_managers, "add_slave_manager": _0_RTM.Manager._d_add_slave_manager, "remove_slave_manager": _0_RTM.Manager._d_remove_slave_manager, "fork": _0_RTM.Manager._d_fork, "shutdown": _0_RTM.Manager._d_shutdown, "restart": _0_RTM.Manager._d_restart, "get_service": _0_RTM.Manager._d_get_service}

Manager._omni_skeleton = Manager
_0_RTM__POA.Manager = Manager
omniORB.registerSkeleton(Manager._NP_RepositoryId, Manager)
del Manager
__name__ = "RTM"

#
# End of module "RTM"
#
__name__ = "Manager_idl"

_exported_modules = ( "RTM", )

# The end.