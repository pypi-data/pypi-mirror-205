#
# Copyright (C) Niel Clausen 2020. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#

# Python imports
import argparse
import json
import os.path
from pathlib import Path
import subprocess

# pywin32 imports
import pywintypes
import win32file

# wxWidgets imports
import wx

# Application imports
from NlvCore.Logmeta import GetMetaStore
from NlvCore.Shell import G_Shell



## PRIVATE #################################################

_Border = 5
_Spacer = 10



## G_FileDropTarget ########################################

class G_FileDropTarget(wx.FileDropTarget):

    #-------------------------------------------------------
    def __init__(self, handler):
        wx.FileDropTarget.__init__(self)
        self._Handler = handler


    #-------------------------------------------------------
    def OnDropFiles(self, x, y, files):
        return self._Handler(files)



## G_Action ################################################

class G_Action(wx.StaticBoxSizer):

    #-------------------------------------------------------
    def __init__(self, parent, label):
        self._Label = label
        super().__init__(wx.VERTICAL, parent, label = label)


    #-------------------------------------------------------
    def GetWindow(self):
        return self.GetStaticBox()


    #-------------------------------------------------------
    def BuildControls(self, ctrls):
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.Add(hsizer, flag = wx.ALL | wx.EXPAND, border = _Border)

        for ctrl in ctrls:
            if isinstance(ctrl, str):
                label = wx.StaticText(self.GetWindow(), label = ctrl)
                hsizer.Add(label, flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)

            elif isinstance(ctrl, int):
                hsizer.AddSpacer(ctrl)

            else:
                hsizer.Add(ctrl, flag = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL)


    #-------------------------------------------------------
    def BuildLabelledRow(self, name, ctrl):
        self.BuildControls([name, _Spacer, ctrl])


    #-------------------------------------------------------
    def CalcLogCmd(self, schema, builder):
        path = "{path}@{schema}".format(path = self._Label, schema = schema)
        if builder is not None:
            path += "@" + builder
        return ["--log", path]



## G_SessionAction #########################################

class G_SessionAction(G_Action):

    #-------------------------------------------------------
    def __init__(self, parent, path_descs):
        super().__init__(parent, "NLV Session File")

        suffix = G_Shell.Extension()

        session_names = []
        if len(path_descs) == 1:
            p = path_descs[0][0]
            common_dir = p.parent
            session_names.append(p.with_suffix(suffix).name)
        else:
            common_dir = Path(os.path.commonpath([str(p[0]) for p in path_descs]))

        # convert .parents to a real list
        candidate_dirs = [common_dir] + [dir for dir in common_dir.parents]
        num_parents = len(candidate_dirs)

        if num_parents == 1:
            # root directory, e.g. C:\
            session_dirs = candidate_dirs
        else:
            want_parents = min(num_parents - 1, 3)
            session_dirs = candidate_dirs[:want_parents]
            for dir in session_dirs:
                session_names.append(dir.with_suffix(suffix).name)

        if len(session_names) == 0:
            session_names.append("session" + suffix)

        window = self.GetWindow()
        self._DirectoryCombo = directory_combo = wx.ComboBox(window,
            choices = [str(dir) for dir in session_dirs],
            style = wx.CB_DROPDOWN
                | wx.CB_READONLY
        )
        directory_combo.SetSelection(0)
        self.BuildLabelledRow("Save in directory", directory_combo)

        self._NameCombo = name_combo = wx.ComboBox(window,
            choices = session_names[:3],
            style = wx.CB_DROPDOWN
                | wx.CB_READONLY
        )
        name_combo.SetSelection(0)
        self.BuildLabelledRow("Session file name", name_combo)


    #-------------------------------------------------------
    def CalcCmd(self):
        dir = self._DirectoryCombo.GetStringSelection()
        name = self._NameCombo.GetStringSelection()
        return ["--new", dir + "\\" + name]



## G_LogFixedAction ########################################

class G_LogFixedAction(G_Action):

    #-------------------------------------------------------
    def __init__(self, parent, path_desc):
        super().__init__(parent, str(path_desc[0]))

        self._Cmd = self.CalcLogCmd(path_desc[1], path_desc[2])
        schema = GetMetaStore().GetLogSchema(path_desc[1])
        builder = schema.GetBuilders().GetObjectByGuid(path_desc[2])

        window = self.GetWindow()
        
        schemata_text = wx.TextCtrl(window,
            size = (200, -1),
            value = schema.GetName(),
            style = wx.TE_READONLY
        )

        builder_text = wx.TextCtrl(window,
            size = (200, -1),
            value = builder.GetName(),
            style = wx.TE_READONLY
        )

        self.BuildControls([
            "Schema", _Spacer, schemata_text,
            2 * _Spacer,
            "Initial view(s)", _Spacer, builder_text
        ])


    #-------------------------------------------------------
    def CalcCmd(self):
        return self._Cmd



## G_LogUserAction #########################################

class G_LogUserAction(G_Action):

    #-------------------------------------------------------
    def __init__(self, parent, path, schemata):
        super().__init__(parent, str(path))

        self._Schemata = schemata
        self._SchemaIdx = 0
        self._BuilderIdx = wx.NOT_FOUND 
        window = self.GetWindow()
        
        schemata_combo = wx.ComboBox(window,
            size = (200, -1),
            choices = [schema.GetName() for schema in schemata],
            style = wx.CB_DROPDOWN
                | wx.CB_READONLY
        )
        schemata_combo.SetSelection(self._SchemaIdx)
        schemata_combo.Bind(wx.EVT_COMBOBOX, self.OnSchema)

        builder_combo = self._BuilderCombo = wx.ComboBox(window,
            size = (200, -1),
            style = wx.CB_DROPDOWN
                | wx.CB_READONLY
        )
        builder_combo.Bind(wx.EVT_COMBOBOX, self.OnBuilder)
        self.SetupBuilderCombo()

        self.BuildControls([
            "Schema", _Spacer, schemata_combo,
            2 * _Spacer,
            "Initial view(s)", _Spacer, builder_combo
        ])


    #-------------------------------------------------------
    def OnSchema(self, event):
        idx = event.GetSelection()
        if idx != self._SchemaIdx:
            self._SchemaIdx = idx
            self.SetupBuilderCombo()


    #-------------------------------------------------------
    def SetupBuilderCombo(self):
        builders = self._Builders = self._Schemata[self._SchemaIdx].GetBuildersNameGuidList()
        if len(builders) == 0:
            self._BuilderCombo.Clear()
            self._BuilderIdx = wx.NOT_FOUND 
        else:
            self._BuilderCombo.SetItems([name for (name, guid) in builders])
            self._BuilderIdx = 0

        self._BuilderCombo.SetSelection(self._BuilderIdx)

    def OnBuilder(self, event):
        self._BuilderIdx = event.GetSelection()


    #-------------------------------------------------------
    def CalcCmd(self):
        schema = self._Schemata[self._SchemaIdx].Guid
        builder = None
        if self._BuilderIdx != wx.NOT_FOUND:
            builder = self._Builders[self._BuilderIdx][1]

        return self.CalcLogCmd(schema, builder)



## G_LaunchFrame ###########################################

class G_LaunchFrame(wx.Frame):

    _DropperText = "Drop log file(s) here"


    #-------------------------------------------------------
    def __init__(self, parent, title, extensions, schemata):
        super().__init__(
            parent, -1, title,
            size = (720, 970),
            style = wx.DEFAULT_FRAME_STYLE
                | wx.NO_FULL_REPAINT_ON_RESIZE
        )

        self._Extensions = extensions
        self._Schemata = schemata

        icon_path = G_Shell.GetLaunchIconPath()
        if icon_path.exists():
            self.SetIcons(wx.IconBundle(str(icon_path)))

        self.SetupUI()

        global _Args
        if _Args.launch is not None:
            self.SetupActions([_Args.launch])


    #-------------------------------------------------------
    def SetupUI(self):
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(frame_sizer)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        dropper_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = "File(s) to launch")
        frame_sizer.Add(dropper_sizer, flag = wx.ALL | wx.EXPAND, border = _Border)
        dropper_window = dropper_sizer.GetStaticBox()

        path_ctrl = self._PathCtrl = wx.StaticText(dropper_window, label = self._DropperText)
        path_ctrl.SetDropTarget(G_FileDropTarget(self.OnDropFiles))
        dropper_sizer.Add(path_ctrl, flag = wx.ALL | wx.EXPAND, border = _Border)

        actions = self._Actions = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(actions, flag = wx.ALL | wx.EXPAND, border = _Border)

        action_sizer = wx.StaticBoxSizer(wx.HORIZONTAL, self, label = "Action")
        frame_sizer.Add(action_sizer, flag = wx.ALL | wx.EXPAND, border = _Border)
        action_window = action_sizer.GetStaticBox()

        global _Args
        self._CloseAfterLaunch = _Args.launch is not None
        close_chkbox = wx.CheckBox(action_window, label = "Close after launch")
        close_chkbox.SetValue(self._CloseAfterLaunch)
        close_chkbox.Bind(wx.EVT_CHECKBOX, self.OnCloseCheck)
        action_sizer.Add(close_chkbox, flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = _Border)

        launch_btn = wx.Button(action_window, label = "Launch")
        launch_btn.Bind(wx.EVT_BUTTON, self.OnLaunch)
        action_sizer.Add(launch_btn, flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = _Border)

        if _Args.debug:
            debug_sizer = wx.StaticBoxSizer(wx.VERTICAL, self, label = "Debug")
            frame_sizer.Add(debug_sizer, flag = wx.ALL | wx.EXPAND, border = _Border)
            debug_window = debug_sizer.GetStaticBox()

            update_btn = wx.Button(debug_window, label = "Update")
            update_btn.Bind(wx.EVT_BUTTON, self.OnUpdate)
            debug_sizer.Add(update_btn, flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, border = _Border)

            debug_ctrl = self._DebugCtrl = wx.StaticText(debug_window)
            debug_sizer.Add(debug_ctrl, flag = wx.ALL | wx.EXPAND, border = _Border)

        self.CenterOnScreen()


    #-------------------------------------------------------
    def GetActions(self):
        return [sizer_item.GetSizer() for sizer_item in self._Actions]


    #-------------------------------------------------------
    def Reset(self):
        frame_sizer = self.GetSizer()

        # seem to have to remove child window(s) manually
        for action in self.GetActions():
            action.GetStaticBox().DestroyChildren()
        frame_sizer.Remove(self._Actions)

        actions = self._Actions = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Insert(1, actions, flag = wx.ALL | wx.EXPAND, border = _Border)
        self._PathCtrl.SetLabel(self._DropperText)


    #-------------------------------------------------------
    def SearchDir(self, dir):
        res = []

        for extension in self._Extensions:
            for searcher in extension._DirectorySearch:
                res += searcher(dir)

        return res
            

    #-------------------------------------------------------
    def ExpandPaths(self, paths):
        """
        Expand the list of paths (strings) to a list of path
        descriptions. Each description is either a tuple containing
        just a pathlib Path, or a tuple of a pathlib path, schema
        GUID and builder GUID.
        """
        res = []

        for p in paths:
            path = Path(p)
            if path.is_file():
                res.append((path,))
            elif path.is_dir():
                res.extend(self.SearchDir(path))

        return res


    #-------------------------------------------------------
    def AddAction(self, action):
        self._Actions.Add(action, flag = wx.TOP | wx.BOTTOM | wx.EXPAND, border = _Border)


    def SetupActions(self, paths):
        self.Reset()

        path_descs = self.ExpandPaths(paths)
        self.AddAction(G_SessionAction(self, path_descs))

        actionable_paths = []
        for path_desc in path_descs:
            path = path_desc[0]
            if len(path_desc) == 1:
                # normal case; user chooses schema and builder
                suffix = path.suffix[1:]
                schemata = self._Schemata.get(suffix)
                if schemata is not None:
                    actionable_paths.append(str(path))
                    self.AddAction(G_LogUserAction(self, path, schemata))

            else:
                # special case; schema and builder are pre-determined
                actionable_paths.append(str(path))
                self.AddAction(G_LogFixedAction(self, path_desc))

        label = self._DropperText
        if len(actionable_paths) != 0:
            label = ",\n".join(actionable_paths)
        self._PathCtrl.SetLabel(label)


    #-------------------------------------------------------
    def OnDropFiles(self, paths):
        self.SetupActions(paths)
        self.GetSizer().Layout()
        return True


    #-------------------------------------------------------
    def OnCloseCheck(self, event):
        self._CloseAfterLaunch = event.GetInt()


    #-------------------------------------------------------
    def CalcCmd(self):
        cmds = [G_Shell().GetInstalledAppPath()]
        for action in self.GetActions():
            cmds += action.CalcCmd()
        return cmds


    def OnLaunch(self, event):
        cmds = self.CalcCmd()

        pipe_open = False
        try:
            handle = win32file.CreateFile(r"\\.\pipe\nlv-cmd", win32file.GENERIC_WRITE, 0, None, win32file.OPEN_EXISTING, 0, None)
            pipe_open = True
    
            encoded_cmds = bytes(json.dumps(cmds[1:]), encoding = "utf-8")
            win32file.WriteFile(handle, encoded_cmds)
            handle.Close()

        except pywintypes.error as werr:
            if not pipe_open:
                subprocess.Popen(self.CalcCmd())

        except Exception as ex:
            pass

        if self._CloseAfterLaunch:
            self.Close()


    #-------------------------------------------------------
    def OnUpdate(self, event):
        self._DebugCtrl.SetLabel("\n".join(self.CalcCmd()))
        self.GetSizer().Layout()



## G_LaunchApp #############################################

class G_LaunchApp(wx.App):

    #-------------------------------------------------------
    def OnInit(self):
        # have to manually set the Posix locale
        self._Locale = wx.Locale(wx.LANGUAGE_DEFAULT)

        self.SetAppName("NLV")
        user_dir = Path(wx.StandardPaths.Get().GetUserDataDir())

        appname = "NlvLaunch"
        self.SetAppName(appname)

        self.SetupMetaData(user_dir)
        extensions = self.SetupExtensions()
        schemata = self.SetupSchemata()

        global _Args
        if _Args.integration:
            G_Shell().SetupLaunchIntegration(schemata.keys())
        else:
            G_LaunchFrame(None, appname, extensions, schemata).Show()

        return True


    #-------------------------------------------------------
    def SetupMetaData(self, user_dir):
        from NlvCore.Logmeta import InitMetaStore
        InitMetaStore(user_dir, 0)


    #-------------------------------------------------------
    def SetupExtensions(self):
        from NlvCore.Logmeta import GetMetaStore

        # Interface between NLV plugins (extensions) and the application
        class Context:
            def __init__(self, info):
                self._Info = info
                info._Converters = []
                info._DirectorySearch = []

            def RegisterLogSchemata(self, install_dir):
                GetMetaStore().RegisterLogSchemata(install_dir)

            def RegisterThemeDirectory(self, install_dir):
                pass

            def RegisterFileConverter(self, extension, converter):
                self._Info._Converters.append((extension, converter))

            def RegisterDirectorySearch(self, searcher):
                self._Info._DirectorySearch.append(searcher)


        # load site specific extensions
        from NlvCore.Extension import LoadExtensions
        return LoadExtensions(Context)


    #-------------------------------------------------------
    def SetupSchemata(self):
        meta_store = GetMetaStore()
        schema_list = [meta_store.GetLogSchema(guid) for (name, guid) in meta_store.GetLogSchemataNames()]

        schemata = dict()
        for schema in schema_list:
            schemata.setdefault(schema.GetExtension(), []).append(schema)

        return schemata



## COMMAND LINE ############################################

_Parser = argparse.ArgumentParser( prog = "launch", description = "NlvLaunch" )
_Parser.add_argument( "-d", "--debug", action = "store_true", help = "debug support" )
_Parser.add_argument( "-i", "--integration", action = "store_true", help = "integrate Launcher into the shell" )
_Parser.add_argument( "-l", "--launch", type = str, default = None, help = "launch file(s)" )
_Args = _Parser.parse_args()



## MODULE ##################################################

def main():
    G_LaunchApp().MainLoop()

if __name__ == "__main__":
    main()
