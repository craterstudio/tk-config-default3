# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
App Launch Hook

This hook is executed to launch the applications.
"""

import os
import tank
import sgtk

logger=sgtk.platform.get_logger(__name__)

class AppLaunch(tank.Hook):
    """
    Hook to run an application.
    """

    def execute(
        self, app_path, app_args, version, engine_name, software_entity=None, **kwargs
    ):
        """
        The execute function of the hook will be called to start the required application

        :param app_path: (str) The path of the application executable
        :param app_args: (str) Any arguments the application may require
        :param version: (str) version of the application being run if set in the
            "versions" settings of the Launcher instance, otherwise None
        :param engine_name (str) The name of the engine associated with the
            software about to be launched.
        :param software_entity: (dict) If set, this is the Software entity that is
            associated with this launch command.

        :returns: (dict) The two valid keys are 'command' (str) and 'return_code' (int).
        """
        loggerinfo=["tk-multi-launchapp", "app_launch"," >>>>> "]
        environtest=os.environ["TK_TEST"]
        environdirlcla=os.environ["DIR_LCLA"]
        environhxaa=os.environ["TK_HXAA"]
        environmyaa=os.environ["TK_MYAA"]
        environnkaa=os.environ["TK_NKAA"]
        environcallapp="CALL_APP"
        hxveraa=os.environ["TK_VER_HXAA"]
        myveraa=os.environ["TK_VER_MYAA"]
        nkveraa=os.environ["TK_VER_NKAA"]
        hxengine=os.environ["TK_TK_HX"]
        myengine=os.environ["TK_TK_MY"]
        nkengine=os.environ["TK_TK_NK"]
        pathtstbat="%s\\pipeline\\crater-meta\\lib\\cs_studio3\\p3_start_local_process.bat"
        pathtstbatnk="%s\\pipeline\\crater-meta\\lib\\cs_studio3\\p3_start_local_sg3nk13.bat"
        otherinfo=None

        pathtstbat=pathtstbat % environdirlcla
        pathtstbatnk=pathtstbatnk % environdirlcla
        otherinfo=[version,environtest,type(environtest),app_path,app_args,engine_name,pathtstbat]

        loggerinfo.extend(otherinfo)

        logger.debug("%s %s %s %s %s %s %s %s %s %s" % tuple(loggerinfo))

        if ((engine_name==hxengine) and (version==hxveraa)):
            # going to use some version of houdinifx
            os.environ[environcallapp]=environhxaa
        elif ((engine_name==myengine) and (version==myveraa)):
            # going to use some version of maya
            os.environ[environcallapp]=environmyaa
        elif ((engine_name==nkengine) and (version==nkveraa)):
            # going to use some version of nk
            os.environ[environcallapp]=environnkaa

        if tank.util.is_linux():
            # on linux, we just run the executable directly
            cmd = "%s %s &" % (app_path, app_args)

        elif tank.util.is_macos():
            # If we're on OS X, then we have two possibilities: we can be asked
            # to launch an application bundle using the "open" command, or we
            # might have been given an executable that we need to treat like
            # any other Unix-style command. The best way we have to know whether
            # we're in one situation or the other is to check the app path we're
            # being asked to launch; if it's a .app, we use the "open" command,
            # and if it's not then we treat it like a typical, Unix executable.
            if app_path.endswith(".app"):
                # The -n flag tells the OS to launch a new instance even if one is
                # already running. The -a flag specifies that the path is an
                # application and supports both the app bundle form or the full
                # executable form.
                cmd = 'open -n -a "%s"' % (app_path)
                if app_args:
                    cmd += " --args %s" % app_args
            else:
                cmd = "%s %s &" % (app_path, app_args)

        else:
            # on windows, we run the start command in order to avoid
            # any command shells popping up as part of the application launch.
            if environtest == "TRUE":
                cmd = 'start /B "App" "%s" %s' % (pathtstbatnk, "\"%s\" %s" % (app_path, app_args))
            else:
                cmd = 'start /B "App" "%s" %s' % (app_path, app_args)

        # run the command to launch the app
        exit_code = os.system(cmd)

        return {"command": cmd, "return_code": exit_code}

