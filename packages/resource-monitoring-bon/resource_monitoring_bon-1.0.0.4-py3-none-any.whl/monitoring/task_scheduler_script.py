# Uses the COM Task Scheduler Interface to create a task
# scheduled to execute when the current user logs on.

import win32com.client
import os

import winreg

def task_scheduler_main():
    # Set the variable name and value
    var_name = "RESOURCE_TASK"
    var_value = os.path.dirname(os.path.abspath(__file__))

    # Set the variable in the current process
    os.environ[var_name] = var_value

    # Open the user environment variables registry key
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)

    # Set the variable in the registry
    winreg.SetValueEx(key, var_name, 0, winreg.REG_SZ, var_value)

    # Close the registry key
    winreg.CloseKey(key)

    computer_name = "" #leave all blank for current computer, current user
    computer_username = ""
    computer_userdomain = ""
    computer_password = ""
    action_id = "Resource_task" #arbitrary action ID
    action_path = r"{}\resource_monitoring.bat".format(os.getenv('RESOURCE_TASK')) #executable path (could be python.exe)
    action_arguments = r'' #arguments (could be something.py)
    action_workdir = os.getenv('RESOURCE_TASK')  #working directory for action executable
    author = "BS" #so that end users know who you are
    description = "Run .bat when the current user logs on"
    task_id = "Resource_task"
    task_hidden = False #set this to True to hide the task in the interface
    username = ""
    password = ""

    #define constants
    TASK_TRIGGER_LOGON = 9
    TASK_CREATE_OR_UPDATE = 6
    TASK_ACTION_EXEC = 0
    TASK_LOGON_INTERACTIVE_TOKEN = 3

    #connect to the scheduler (Vista/Server 2008 and above only)
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect(computer_name or None, computer_username or None, computer_userdomain or None, computer_password or None)
    rootFolder = scheduler.GetFolder("\\")

    #(re)define the task
    taskDef = scheduler.NewTask(0)
    colTriggers = taskDef.Triggers

    trigger = colTriggers.Create(TASK_TRIGGER_LOGON)
    trigger.Id = "BootTriggerId"
    trigger.UserId = os.environ.get('USERNAME') # current user account
    #trigger.Enabled = False

    colActions = taskDef.Actions
    action = colActions.Create(TASK_ACTION_EXEC)
    action.ID = action_id
    action.Path = action_path
    action.WorkingDirectory = action_workdir
    action.Arguments = action_arguments

    info = taskDef.RegistrationInfo
    info.Author = author
    info.Description = description

    settings = taskDef.Settings
    #settings.Enabled = False
    settings.Hidden = task_hidden
    settings.AllowHardTerminate = False
    settings.ExecutionTimeLimit = "PT0S"
    #settings.StartWhenAvailable = True

    #register the task (create or update, just keep the task name the same)
    result = rootFolder.RegisterTaskDefinition(task_id, taskDef, TASK_CREATE_OR_UPDATE, "", "", TASK_LOGON_INTERACTIVE_TOKEN)

if __name__ == "__main__":
    task_scheduler_main()