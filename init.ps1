$TargetFilename = "python-lambda-template"
$TargetPackageFilename = $TargetFilename.replace("-", "_")
$TargetDomain = "domain.com"

$DesiredFilename = Read-Host "Please specify new project name: "
$DesiredPackageName = $DesiredFilename.replace("-", "_")
$DesiredDomain = Read-Host "Please specify api parent domain e.g. <apiparentdomain.com>: "

Set-Location $PSScriptRoot

Get-ChildItem $PSScriptRoot -File | ForEach-Object {
    (Get-Content $_)-replace($TargetFilename,$DesiredFilename) | Set-Content $_
    (Get-Content $_)-replace($TargetPackageFilename,$DesiredPackageName) | Set-Content $_
    (Get-Content $_)-replace($TargetDomain,$DesiredDomain) | Set-Content $_
}

Get-ChildItem $PSScriptRoot -Recurse |
Where-Object { $_.Name -eq $TargetFilename} |
ForEach-Object { Rename-Item $_ -NewName $DesiredName }

Get-ChildItem $PSScriptRoot -Recurse |
Where-Object { $_.Name -eq $TargetPackageFilename} |
ForEach-Object { Rename-Item $_ -NewName $DesiredPackageName }
