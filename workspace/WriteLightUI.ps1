$parDir = Split-Path -Parent $PSScriptRoot

pyuic5 -x "$PSScriptRoot\LightUI.ui" -o "$PSScriptRoot\LightUI.py"
pyrcc5 "$PSScriptRoot\LightUIRes.qrc" -o "$PSScriptRoot\LightUIRes_rc.py"

Copy-Item -Path "$PSScriptRoot\LightUI.py" -Destination "$parDir\light_ui_TEMP.py" -Force
Copy-Item -Path "$PSScriptRoot\LightUIRes_rc.py" -Destination "$parDir\light_ui_res_TEMP.py" -Force

$patternEmpty = "(import LightUIRes_rc[\S\s]*exec_\(\)\))"

$lightUiArrText = Get-Content "$parDir\light_ui_TEMP.py"
$lightUiText = [string]::Join([Environment]::NewLine, $lightUiArrText)

$newLightUiText = [Regex]::Replace($lightUiText, $patternEmpty, "import light_ui_res")
Set-Content "$parDir\light_ui_TEMP.py" $newLightUiText