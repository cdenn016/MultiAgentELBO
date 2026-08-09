[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,

    [Parameter(Mandatory = $true)]
    [string]$SourceDirectory,

    [Parameter(Mandatory = $true)]
    [string]$RepositoryBuildScript,

    [Parameter(Mandatory = $true)]
    [string]$ExecutedBuildScript,

    [Parameter(Mandatory = $true)]
    [string]$BootstrapAttestationPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputDirectory,

    [Parameter(Mandatory = $true)]
    [string]$AuditPath,

    [Parameter(Mandatory = $true)]
    [string]$SourceRevision,

    [Parameter(Mandatory = $true)]
    [string]$VerificationResult,

    [Parameter(Mandatory = $true)]
    [string]$VerificationReport,

    [Parameter(Mandatory = $true)]
    [string]$PdflatexPath,

    [Parameter(Mandatory = $true)]
    [string]$BibtexPath,

    [Parameter(Mandatory = $true)]
    [string]$BibtexStylePath
)

$ErrorActionPreference = 'Stop'
$InvariantCulture = [System.Globalization.CultureInfo]::InvariantCulture
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$ProductionProfile = 'gauge-vfe-rg-production-v1'
$PythonPath = 'C:\Python314\python.exe'
$GitPath = 'C:\Program Files\Git\cmd\git.exe'
$PypdfSitePath = 'C:\Users\chris and christine\AppData\Roaming\Python\Python314\site-packages'
$PypdfPackagePath = Join-Path -Path $PypdfSitePath -ChildPath 'pypdf'
$ExpectedPypdfVersion = '6.12.2'
$WindowsDirectory = 'C:\WINDOWS'
$SystemDirectory = 'C:\WINDOWS\System32'
$PowerShellPath = 'C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe'
$PythonChildTempDirectory = $null
$PythonChildAdditionalEnvironment = [ordered]@{}
$PypdfPycacheCleanupPath = $null
$ExternalInputDiscoveryLimit = 8

if ($PSCommandPath) {
    throw 'Authenticated in-memory child unexpectedly has PSCommandPath.'
}

$ExpectedBuildEnvironment = [ordered]@{
    GAUGE_VFE_BUILD_REPOSITORY_ROOT = $RepositoryRoot
    GAUGE_VFE_BUILD_SOURCE_DIRECTORY = $SourceDirectory
    GAUGE_VFE_BUILD_REPOSITORY_BUILD_SCRIPT = $RepositoryBuildScript
    GAUGE_VFE_BUILD_EXECUTED_BUILD_SCRIPT = $ExecutedBuildScript
    GAUGE_VFE_BUILD_BOOTSTRAP_ATTESTATION_PATH = $BootstrapAttestationPath
    GAUGE_VFE_BUILD_OUTPUT_DIRECTORY = $OutputDirectory
    GAUGE_VFE_BUILD_AUDIT_PATH = $AuditPath
    GAUGE_VFE_BUILD_SOURCE_REVISION = $SourceRevision
    GAUGE_VFE_BUILD_VERIFICATION_RESULT = $VerificationResult
    GAUGE_VFE_BUILD_VERIFICATION_REPORT = $VerificationReport
    GAUGE_VFE_BUILD_PDFLATEX_PATH = $PdflatexPath
    GAUGE_VFE_BUILD_BIBTEX_PATH = $BibtexPath
    GAUGE_VFE_BUILD_BIBTEX_STYLE_PATH = $BibtexStylePath
}
$expectedBuildEnvironmentNames = [string[]]@($ExpectedBuildEnvironment.Keys)
[System.Array]::Sort(
    $expectedBuildEnvironmentNames,
    [System.StringComparer]::Ordinal
)
$actualBuildEnvironmentNames = [string[]]@(
    Get-ChildItem Env: |
        Where-Object {
            $_.Name.StartsWith(
                'GAUGE_VFE_BUILD_',
                [System.StringComparison]::OrdinalIgnoreCase
            )
        } |
        ForEach-Object { [string]$_.Name }
)
[System.Array]::Sort(
    $actualBuildEnvironmentNames,
    [System.StringComparer]::Ordinal
)
if (
    (@($actualBuildEnvironmentNames) -join "`n") -cne
    (@($expectedBuildEnvironmentNames) -join "`n")
) {
    throw 'Authenticated child requires the exact GAUGE_VFE_BUILD_ environment schema.'
}
foreach ($name in @($expectedBuildEnvironmentNames)) {
    if (
        [string][System.Environment]::GetEnvironmentVariable($name) -cne
        [string]$ExpectedBuildEnvironment[$name]
    ) {
        throw "Authenticated child environment value does not equal parameter $name."
    }
}

if (-not ('GaugeVfeExecutableHandleIdentity' -as [type])) {
    Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Globalization;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

public static class GaugeVfeExecutableHandleIdentity
{
    [StructLayout(LayoutKind.Sequential)]
    private struct FileTime
    {
        public uint Low;
        public uint High;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct ByHandleFileInformation
    {
        public uint FileAttributes;
        public FileTime CreationTime;
        public FileTime LastAccessTime;
        public FileTime LastWriteTime;
        public uint VolumeSerialNumber;
        public uint FileSizeHigh;
        public uint FileSizeLow;
        public uint NumberOfLinks;
        public uint FileIndexHigh;
        public uint FileIndexLow;
    }

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool GetFileInformationByHandle(
        SafeFileHandle handle,
        out ByHandleFileInformation information
    );

    private static ulong Join(uint high, uint low)
    {
        return ((ulong)high << 32) | low;
    }

    public static string[] GetIdentity(SafeFileHandle handle)
    {
        ByHandleFileInformation information;
        if (!GetFileInformationByHandle(handle, out information))
        {
            throw new Win32Exception(Marshal.GetLastWin32Error());
        }
        return new[]
        {
            information.VolumeSerialNumber.ToString(CultureInfo.InvariantCulture),
            Join(information.FileIndexHigh, information.FileIndexLow).ToString(CultureInfo.InvariantCulture),
            Join(information.FileSizeHigh, information.FileSizeLow).ToString(CultureInfo.InvariantCulture),
            Join(information.CreationTime.High, information.CreationTime.Low).ToString(CultureInfo.InvariantCulture),
            Join(information.LastWriteTime.High, information.LastWriteTime.Low).ToString(CultureInfo.InvariantCulture),
            information.FileAttributes.ToString(CultureInfo.InvariantCulture),
            information.NumberOfLinks.ToString(CultureInfo.InvariantCulture)
        };
    }
}
'@
}

function Open-ExecutableLaunchLock {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    Assert-NoReparseComponents -Path $Path -Label 'Executable launch lock'
    return [System.IO.FileStream]::new(
        $Path,
        [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::Read,
        4096,
        [System.IO.FileOptions]::RandomAccess
    )
}

function Get-LockedExecutableSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [System.IO.FileStream]$Stream
    )

    $digest = [System.Security.Cryptography.SHA256]::Create()
    try {
        $Stream.Position = 0
        $hashBytes = $digest.ComputeHash($Stream)
        $hash = ([System.BitConverter]::ToString($hashBytes)).Replace('-', '').ToLowerInvariant()
        $byteCount = [int64]$Stream.Length
        $handleIdentity = @(
            [GaugeVfeExecutableHandleIdentity]::GetIdentity($Stream.SafeFileHandle)
        )
    }
    finally {
        $digest.Dispose()
        $Stream.Position = 0
    }
    return [ordered]@{
        path = [System.IO.Path]::GetFullPath($Path)
        sha256 = $hash
        byte_count = $byteCount
        handle_identity = $handleIdentity
    }
}

function Assert-LockedExecutableSnapshotEqual {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Expected,
        [Parameter(Mandatory = $true)]
        [object]$Actual,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if (
        [string]$Actual.path -cne [string]$Expected.path -or
        [string]$Actual.sha256 -cne [string]$Expected.sha256 -or
        [int64]$Actual.byte_count -ne [int64]$Expected.byte_count -or
        (@($Actual.handle_identity) -join ',') -cne (@($Expected.handle_identity) -join ',')
    ) {
        throw "$Label held-handle bytes or filesystem identity changed from launch-lock M0."
    }
}

function Invoke-TrustedPythonCapture {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $entry = $ExecutableLaunchLocks.python_executable
    $before = Get-LockedExecutableSnapshot -Path $PythonPath -Stream $entry.Stream
    Assert-LockedExecutableSnapshotEqual -Expected $entry.Snapshot -Actual $before -Label $Label
    try {
        $childEnvironment = Get-ClosedChildEnvironment `
            -Executable $PythonPath `
            -TempDirectory $PythonChildTempDirectory `
            -Additional $PythonChildAdditionalEnvironment
        $invocation = Invoke-ExplicitChildProcess `
            -Executable $PythonPath `
            -Arguments $Arguments `
            -WorkingDirectory ([System.IO.Path]::GetFullPath((Get-Location).Path)) `
            -Environment $childEnvironment
        $output = $invocation.Output
        $exitCode = $invocation.ExitCode
        if ($invocation.Error) {
            [Console]::Error.Write([string]$invocation.Error)
        }
    }
    finally {
        $after = Get-LockedExecutableSnapshot -Path $PythonPath -Stream $entry.Stream
        Assert-LockedExecutableSnapshotEqual -Expected $entry.Snapshot -Actual $after -Label $Label
    }
    return [pscustomobject]@{
        Output = [string]$output
        ExitCode = [int]$exitCode
    }
}

function ConvertTo-WindowsCommandLineArgument {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$Value
    )

    $builder = New-Object System.Text.StringBuilder
    [void]$builder.Append('"')
    $backslashes = 0
    foreach ($character in $Value.ToCharArray()) {
        if ($character -eq '\') {
            $backslashes++
            continue
        }
        if ($character -eq '"') {
            [void]$builder.Append(('\' * (2 * $backslashes + 1)))
            [void]$builder.Append('"')
            $backslashes = 0
            continue
        }
        if ($backslashes -ne 0) {
            [void]$builder.Append(('\' * $backslashes))
            $backslashes = 0
        }
        [void]$builder.Append($character)
    }
    if ($backslashes -ne 0) {
        [void]$builder.Append(('\' * (2 * $backslashes)))
    }
    [void]$builder.Append('"')
    return $builder.ToString()
}

function Get-ClosedChildEnvironment {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [Parameter(Mandatory = $true)]
        [string]$TempDirectory,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$Additional
    )

    $environment = [ordered]@{
        SystemRoot = $WindowsDirectory
        WINDIR = $WindowsDirectory
        SystemDrive = 'C:'
        COMSPEC = Join-Path -Path $SystemDirectory -ChildPath 'cmd.exe'
        PATHEXT = '.COM;.EXE;.BAT;.CMD'
        PATH = @(
            [System.IO.Path]::GetDirectoryName($Executable),
            $SystemDirectory
        ) -join ';'
        TEMP = $TempDirectory
        TMP = $TempDirectory
    }
    foreach ($name in @($Additional.Keys)) {
        if ($environment.Contains([string]$name)) {
            throw "Additional child environment duplicates fixed key $name."
        }
        $environment[[string]$name] = [string]$Additional[$name]
    }
    return $environment
}

function Invoke-ExplicitChildProcess {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [string]$WorkingDirectory,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$Environment
    )

    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $Executable
    $startInfo.Arguments = @(
        $Arguments | ForEach-Object { ConvertTo-WindowsCommandLineArgument -Value $_ }
    ) -join ' '
    $startInfo.WorkingDirectory = $WorkingDirectory
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.StandardOutputEncoding = [System.Text.Encoding]::UTF8
    $startInfo.StandardErrorEncoding = [System.Text.Encoding]::UTF8
    $startInfo.EnvironmentVariables.Clear()
    foreach ($name in @($Environment.Keys)) {
        $startInfo.EnvironmentVariables.Add([string]$name, [string]$Environment[$name])
    }
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    try {
        if (-not $process.Start()) {
            throw "Process start returned false for $Executable."
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        $process.WaitForExit()
        $stdout = $stdoutTask.Result
        $stderr = $stderrTask.Result
        $exitCode = $process.ExitCode
    }
    finally {
        $process.Dispose()
    }
    return [pscustomobject]@{
        Output = [string]$stdout
        Error = [string]$stderr
        ExitCode = [int]$exitCode
    }
}

function Get-AbsolutePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value,
        [Parameter(Mandatory = $true)]
        [string]$BaseDirectory
    )

    if ([System.IO.Path]::IsPathRooted($Value)) {
        return [System.IO.Path]::GetFullPath($Value)
    }
    return [System.IO.Path]::GetFullPath((Join-Path -Path $BaseDirectory -ChildPath $Value))
}

function Assert-NoReparseComponents {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $pathRoot = [System.IO.Path]::GetPathRoot($fullPath)
    $relative = $fullPath.Substring($pathRoot.Length)
    $components = $relative.Split(
        [char[]]'\/',
        [System.StringSplitOptions]::RemoveEmptyEntries
    )
    $current = $pathRoot
    foreach ($component in $components) {
        $current = Join-Path -Path $current -ChildPath $component
        if (-not (Test-Path -LiteralPath $current)) {
            break
        }
        $item = Get-Item -LiteralPath $current -Force -ErrorAction Stop
        if (
            ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne
            0
        ) {
            throw "$Label contains a reparse-point or junction component: $current"
        }
    }
}

function Test-PathWithin {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Candidate,
        [Parameter(Mandatory = $true)]
        [string]$Root
    )

    $normalizedRoot = $Root.TrimEnd(
        [System.IO.Path]::DirectorySeparatorChar,
        [System.IO.Path]::AltDirectorySeparatorChar
    )
    $prefix = $normalizedRoot + [System.IO.Path]::DirectorySeparatorChar
    return $Candidate.Equals($normalizedRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
        $Candidate.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)
}

function Get-RepositoryRelativePath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot
    )

    if (-not (Test-PathWithin -Candidate $Path -Root $RepositoryRoot)) {
        throw "Path is outside the repository: $Path"
    }
    $relative = $Path.Substring($RepositoryRoot.Length).TrimStart('\', '/')
    return $relative.Replace('\', '/')
}

function Resolve-Executable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Value,
        [Parameter(Mandatory = $true)]
        [string]$BaseDirectory
    )

    $candidate = Get-AbsolutePath -Value $Value -BaseDirectory $BaseDirectory
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        return $candidate
    }
    $command = Get-Command -Name $Value -CommandType Application -ErrorAction Stop |
        Select-Object -First 1
    $resolved = if ($command.Source) { $command.Source } else { $command.Path }
    if (-not $resolved) {
        throw "Executable '$Value' did not resolve to an application path."
    }
    return [System.IO.Path]::GetFullPath($resolved)
}

function Get-ToolIdentity {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedSnapshot
    )

    $snapshotBefore = Get-ExternalToolRunSnapshot -Path $Executable
    Assert-ExternalToolSnapshotEqual `
        -Expected $ExpectedSnapshot `
        -Actual $snapshotBefore `
        -Label ([System.IO.Path]::GetFileName($Executable))
    $information = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($Executable)
    $version = $information.ProductVersion
    if (-not $version) {
        $version = $information.FileVersion
    }
    $snapshotAfter = Get-ExternalToolRunSnapshot -Path $Executable
    Assert-ExternalToolSnapshotEqual `
        -Expected $ExpectedSnapshot `
        -Actual $snapshotAfter `
        -Label ([System.IO.Path]::GetFileName($Executable))
    $digest = [string]$ExpectedSnapshot.sha256
    if ($version) {
        return "file-version:$version;sha256:$digest"
    }
    return "sha256:$digest"
}

function Get-FileIdentityRecord {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [string]$RepositoryRoot
    )

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    if (
        $item.PSIsContainer -or
        ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
    ) {
        throw "Identity target must be a regular non-reparse file: $Path"
    }
    $recordedPath = if ($RepositoryRoot) {
        Get-RepositoryRelativePath -Path $item.FullName -RepositoryRoot $RepositoryRoot
    }
    else {
        $item.FullName
    }
    return [ordered]@{
        path = $recordedPath
        sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        byte_count = [int64]$item.Length
    }
}

function Get-TrustedExecutableRunSnapshot {
    $snapshotProgram = @'
import hashlib
import json
import os
import pathlib
import stat
import sys

def first_reparse(path):
    absolute = pathlib.Path(os.path.abspath(path))
    parts = absolute.parts
    current = pathlib.Path(parts[0])
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for part in parts[1:]:
        current /= part
        information = current.lstat()
        if current.is_symlink() or bool(getattr(information, "st_file_attributes", 0) & reparse_flag):
            return current
    return None

def identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

def content_identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_size,
        information.st_mtime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

def snapshot(raw_path):
    path = pathlib.Path(raw_path)
    mediated = first_reparse(path)
    if mediated is not None:
        raise RuntimeError(f"trusted executable is reparse-mediated at {mediated}")
    path = path.resolve(strict=True)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise RuntimeError(f"trusted executable is not regular: {path}")
    digest = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if content_identity(before) != content_identity(opened):
            raise RuntimeError(f"trusted executable changed while opening: {path}")
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            byte_count += len(block)
        after_read = os.fstat(stream.fileno())
    after_close = path.lstat()
    if identity(before) != identity(after_close) or content_identity(opened) != content_identity(after_read):
        raise RuntimeError(f"trusted executable changed during hashing: {path}")
    return {
        "path": str(path),
        "sha256": digest.hexdigest(),
        "byte_count": byte_count,
        "stat_identity": identity(after_close),
    }

document = {
    "python_executable": snapshot(sys.argv[1]),
    "git_executable": snapshot(sys.argv[2]),
}
print(json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False))
'@
    $encodedProgram = [System.Convert]::ToBase64String(
        [System.Text.Encoding]::UTF8.GetBytes($snapshotProgram)
    )
    $launcher = "import base64,sys;exec(compile(base64.b64decode(sys.argv.pop(1)),'<executable-snapshot>','exec'))"
    $invocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', '-c', $launcher, $encodedProgram, $PythonPath, $GitPath
    ) -Label 'Trusted executable snapshot Python invocation'
    $output = $invocation.Output
    $exitCode = $invocation.ExitCode
    if ($exitCode -ne 0) {
        throw "Trusted executable snapshot failed with exit code $exitCode."
    }
    try {
        $snapshot = ConvertFrom-Json -InputObject (@($output) -join "`n") -ErrorAction Stop
    }
    catch {
        throw "Trusted executable snapshot is not valid JSON: $($_.Exception.Message)"
    }
    Assert-ExactProperties -Value $snapshot -Expected @(
        'python_executable', 'git_executable'
    ) -Label 'Trusted executable snapshot'
    foreach ($field in @('python_executable', 'git_executable')) {
        Assert-ExactProperties -Value $snapshot.$field -Expected @(
            'path', 'sha256', 'byte_count', 'stat_identity'
        ) -Label "Trusted executable snapshot $field"
        if (
            [string]$snapshot.$field.sha256 -cnotmatch '^[0-9a-f]{64}$' -or
            @($snapshot.$field.stat_identity).Count -ne 7
        ) {
            throw "Trusted executable snapshot $field has an invalid raw identity."
        }
    }
    return $snapshot
}

function Get-PublicExecutableIdentity {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Snapshot
    )

    return [ordered]@{
        path = [string]$Snapshot.path
        sha256 = [string]$Snapshot.sha256
        byte_count = [int64]$Snapshot.byte_count
    }
}

function Get-ExternalToolRunSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $snapshotProgram = @'
import hashlib
import json
import os
import pathlib
import stat
import sys

path = pathlib.Path(sys.argv[1])
absolute = pathlib.Path(os.path.abspath(path))
parts = absolute.parts
current = pathlib.Path(parts[0])
reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
for part in parts[1:]:
    current /= part
    information = current.lstat()
    if current.is_symlink() or bool(getattr(information, "st_file_attributes", 0) & reparse_flag):
        raise RuntimeError(f"external tool path is reparse-mediated at {current}")
path = path.resolve(strict=True)

def identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

def content_identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_size,
        information.st_mtime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

before = path.lstat()
if not stat.S_ISREG(before.st_mode):
    raise RuntimeError(f"external tool is not regular: {path}")
digest = hashlib.sha256()
byte_count = 0
with path.open("rb") as stream:
    opened = os.fstat(stream.fileno())
    if content_identity(before) != content_identity(opened):
        raise RuntimeError(f"external tool changed while opening: {path}")
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
        byte_count += len(block)
    after_read = os.fstat(stream.fileno())
after_close = path.lstat()
if identity(before) != identity(after_close) or content_identity(opened) != content_identity(after_read):
    raise RuntimeError(f"external tool changed during hashing: {path}")
print(
    json.dumps(
        {
            "path": str(path),
            "sha256": digest.hexdigest(),
            "byte_count": byte_count,
            "stat_identity": identity(after_close),
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)
'@
    $encodedProgram = [System.Convert]::ToBase64String(
        [System.Text.Encoding]::UTF8.GetBytes($snapshotProgram)
    )
    $launcher = "import base64,sys;exec(compile(base64.b64decode(sys.argv.pop(1)),'<external-tool-snapshot>','exec'))"
    $invocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', '-c', $launcher, $encodedProgram, $Path
    ) -Label 'External executable snapshot Python invocation'
    $output = $invocation.Output
    $exitCode = $invocation.ExitCode
    if ($exitCode -ne 0) {
        throw "External tool snapshot failed with exit code $exitCode for $Path."
    }
    try {
        $snapshot = ConvertFrom-Json -InputObject (@($output) -join "`n") -ErrorAction Stop
    }
    catch {
        throw "External tool snapshot is not valid JSON: $($_.Exception.Message)"
    }
    Assert-ExactProperties -Value $snapshot -Expected @(
        'path', 'sha256', 'byte_count', 'stat_identity'
    ) -Label 'External tool snapshot'
    if (
        [string]$snapshot.sha256 -cnotmatch '^[0-9a-f]{64}$' -or
        @($snapshot.stat_identity).Count -ne 7
    ) {
        throw 'External tool snapshot has an invalid raw identity.'
    }
    return $snapshot
}

function Assert-ExternalToolSnapshotEqual {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Expected,
        [Parameter(Mandatory = $true)]
        [object]$Actual,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if (
        [string]$Actual.path -cne [string]$Expected.path -or
        [string]$Actual.sha256 -cne [string]$Expected.sha256 -or
        [int64]$Actual.byte_count -ne [int64]$Expected.byte_count -or
        (@($Actual.stat_identity) -join ',') -cne (@($Expected.stat_identity) -join ',')
    ) {
        throw "$Label bytes or filesystem identity changed from driver M0."
    }
}

function Assert-TrustedExecutableSnapshotsEqual {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Before,
        [Parameter(Mandatory = $true)]
        [object]$After
    )

    foreach ($field in @('python_executable', 'git_executable')) {
        $beforeRecord = $Before.$field
        $afterRecord = $After.$field
        if (
            [string]$afterRecord.path -cne [string]$beforeRecord.path -or
            [string]$afterRecord.sha256 -cne [string]$beforeRecord.sha256 -or
            [int64]$afterRecord.byte_count -ne [int64]$beforeRecord.byte_count -or
            (@($afterRecord.stat_identity) -join ',') -cne (@($beforeRecord.stat_identity) -join ',')
        ) {
            throw "Trusted $field bytes or filesystem identity changed between driver M0 and M1."
        }
    }
}

function Invoke-TrustedGit {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot,
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $entry = $ExecutableLaunchLocks.git_executable
    $before = Get-LockedExecutableSnapshot -Path $GitPath -Stream $entry.Stream
    Assert-LockedExecutableSnapshotEqual -Expected $entry.Snapshot -Actual $before -Label $Label
    $metadataM0 = Get-GitMetadataGuardSnapshot -RepositoryRoot $RepositoryRoot
    $metadataM0Repeat = Get-GitMetadataGuardSnapshot -RepositoryRoot $RepositoryRoot
    Assert-GitMetadataGuardSnapshotEqual `
        -Expected $metadataM0 `
        -Actual $metadataM0Repeat `
        -Label "$Label metadata preflight"
    try {
        $gitEnvironment = Get-ClosedChildEnvironment `
            -Executable $GitPath `
            -TempDirectory $PythonChildTempDirectory `
            -Additional ([ordered]@{
                GIT_NO_REPLACE_OBJECTS = '1'
                GIT_CONFIG_NOSYSTEM = '1'
                GIT_CONFIG_GLOBAL = 'NUL'
            })
        $invocation = Invoke-ExplicitChildProcess `
            -Executable $GitPath `
            -Arguments (@('--no-replace-objects', '--literal-pathspecs', '-C', $RepositoryRoot) + @($Arguments)) `
            -WorkingDirectory $RepositoryRoot `
            -Environment $gitEnvironment
        $output = $invocation.Output
        $exitCode = $invocation.ExitCode
        if ($invocation.Error) {
            [Console]::Error.Write([string]$invocation.Error)
        }
    }
    finally {
        $metadataM1 = Get-GitMetadataGuardSnapshot -RepositoryRoot $RepositoryRoot
        Assert-GitMetadataGuardSnapshotEqual `
            -Expected $metadataM0 `
            -Actual $metadataM1 `
            -Label "$Label metadata postflight"
        $after = Get-LockedExecutableSnapshot -Path $GitPath -Stream $entry.Stream
        Assert-LockedExecutableSnapshotEqual -Expected $entry.Snapshot -Actual $after -Label $Label
    }
    if ($exitCode -ne 0) {
        throw "$Label failed with trusted Git exit code $exitCode."
    }
    return ([string]$output).Trim()
}

function Get-GitMetadataDirectories {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot
    )

    $marker = Join-Path -Path $RepositoryRoot -ChildPath '.git'
    Assert-NoReparseComponents -Path $marker -Label 'Git metadata marker'
    if (Test-Path -LiteralPath $marker -PathType Container) {
        $gitDirectory = [System.IO.Path]::GetFullPath($marker)
    }
    elseif (Test-Path -LiteralPath $marker -PathType Leaf) {
        $line = [System.IO.File]::ReadAllText($marker, [System.Text.Encoding]::UTF8).Trim()
        if (-not $line.StartsWith('gitdir: ', [System.StringComparison]::Ordinal)) {
            throw 'Repository .git file has an invalid gitdir record.'
        }
        $value = $line.Substring(8)
        $gitDirectory = Get-AbsolutePath -Value $value -BaseDirectory $RepositoryRoot
        Assert-NoReparseComponents -Path $gitDirectory -Label 'Git directory'
        if (-not (Test-Path -LiteralPath $gitDirectory -PathType Container)) {
            throw "Resolved Git directory is missing: $gitDirectory"
        }
    }
    else {
        throw "Repository has no regular .git metadata marker: $RepositoryRoot"
    }

    $directories = New-Object System.Collections.ArrayList
    [void]$directories.Add($gitDirectory)
    $commonMarker = Join-Path -Path $gitDirectory -ChildPath 'commondir'
    if (Test-Path -LiteralPath $commonMarker) {
        Assert-NoReparseComponents -Path $commonMarker -Label 'Git commondir marker'
        if (-not (Test-Path -LiteralPath $commonMarker -PathType Leaf)) {
            throw 'Git commondir marker must be a regular file.'
        }
        $commonValue = [System.IO.File]::ReadAllText(
            $commonMarker,
            [System.Text.Encoding]::UTF8
        ).Trim()
        $commonDirectory = Get-AbsolutePath -Value $commonValue -BaseDirectory $gitDirectory
        Assert-NoReparseComponents -Path $commonDirectory -Label 'Git common directory'
        if (-not (Test-Path -LiteralPath $commonDirectory -PathType Container)) {
            throw "Resolved Git common directory is missing: $commonDirectory"
        }
        if (-not $commonDirectory.Equals($gitDirectory, [System.StringComparison]::OrdinalIgnoreCase)) {
            [void]$directories.Add($commonDirectory)
        }
    }
    return @($directories)
}

function Assert-NoGitMetadataOverrides {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot
    )

    $relativePaths = @(
        'info/grafts',
        'shallow',
        'objects/info/alternates',
        'objects/info/http-alternates'
    )
    foreach ($metadataRoot in @(Get-GitMetadataDirectories -RepositoryRoot $RepositoryRoot)) {
        foreach ($relative in $relativePaths) {
            $candidate = Join-Path -Path $metadataRoot -ChildPath $relative
            if (-not (Test-Path -LiteralPath $candidate)) {
                continue
            }
            Assert-NoReparseComponents -Path $candidate -Label "Git metadata override $relative"
            $item = Get-Item -LiteralPath $candidate -Force -ErrorAction Stop
            if ($item.PSIsContainer -or $item.Length -ne 0) {
                throw "Forbidden nonempty or nonregular Git metadata override: $relative"
            }
        }
    }
}

function Get-GitMetadataGuardSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot
    )

    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $records = New-Object System.Collections.ArrayList
    $relativeComponents = @(
        '',
        'commondir',
        'info',
        'info/grafts',
        'objects',
        'objects/info',
        'objects/info/alternates',
        'objects/info/http-alternates',
        'shallow'
    )
    foreach ($metadataRoot in @(Get-GitMetadataDirectories -RepositoryRoot $RepositoryRoot)) {
        foreach ($relative in $relativeComponents) {
            $candidate = if ($relative) {
                Join-Path -Path $metadataRoot -ChildPath $relative
            }
            else {
                $metadataRoot
            }
            $fullPath = [System.IO.Path]::GetFullPath($candidate)
            if (-not (Test-Path -LiteralPath $fullPath)) {
                [void]$records.Add([ordered]@{
                    path = $fullPath
                    kind = 'absent'
                })
                continue
            }
            Assert-NoReparseComponents -Path $fullPath -Label 'Git metadata guard component'
            $item = Get-Item -LiteralPath $fullPath -Force -ErrorAction Stop
            $kind = if ($item.PSIsContainer) { 'directory' } else { 'file' }
            $record = [ordered]@{
                path = $item.FullName
                kind = $kind
                attributes = [int64]$item.Attributes
                creation_time_utc_ticks = [int64]$item.CreationTimeUtc.Ticks
                last_write_time_utc_ticks = [int64]$item.LastWriteTimeUtc.Ticks
            }
            if (-not $item.PSIsContainer) {
                $record.byte_count = [int64]$item.Length
                $record.sha256 = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            }
            [void]$records.Add($record)
        }
    }
    return @($records)
}

function Assert-GitMetadataGuardSnapshotEqual {
    param(
        [Parameter(Mandatory = $true)]
        [object[]]$Expected,
        [Parameter(Mandatory = $true)]
        [object[]]$Actual,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $expectedJson = ConvertTo-Json -InputObject @($Expected) -Compress -Depth 5
    $actualJson = ConvertTo-Json -InputObject @($Actual) -Compress -Depth 5
    if ($actualJson -cne $expectedJson) {
        throw "$Label detected a transient or persistent Git metadata change."
    }
}

function Assert-FileBoundToRevision {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$RepositoryRoot,
        [Parameter(Mandatory = $true)]
        [string]$Revision
    )

    $relative = Get-RepositoryRelativePath -Path $Path -RepositoryRoot $RepositoryRoot
    $objectFormat = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'rev-parse', '--show-object-format'
    ) -Label 'Git object-format lookup'
    if ($objectFormat -cne 'sha1') {
        throw "Exact raw-byte source binding requires Git object format sha1; found '$objectFormat'."
    }
    $objectSpec = "${Revision}:$relative"
    $objectType = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'cat-file', '-t', $objectSpec
    ) -Label "Git type lookup for $relative"
    if ($objectType -cne 'blob') {
        throw "Source-revision object is not a blob: $relative"
    }
    $revisionObject = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'rev-parse', '--verify', $objectSpec
    ) -Label "Git object lookup for $relative"

    $rawBytes = [System.IO.File]::ReadAllBytes($Path)
    function Get-RawBlobObjectId {
        param([byte[]]$Bytes)

        $header = [System.Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)`0")
        $payload = New-Object byte[] ($header.Length + $Bytes.Length)
        [System.Array]::Copy($header, 0, $payload, 0, $header.Length)
        [System.Array]::Copy($Bytes, 0, $payload, $header.Length, $Bytes.Length)
        $sha1 = [System.Security.Cryptography.SHA1]::Create()
        try {
            return ([System.BitConverter]::ToString($sha1.ComputeHash($payload))).Replace('-', '').ToLowerInvariant()
        }
        finally {
            $sha1.Dispose()
        }
    }
    $rawObject = Get-RawBlobObjectId -Bytes $rawBytes
    if ($revisionObject -cne $rawObject) {
        throw "Raw worktree bytes are not bound to source revision $Revision`: $relative"
    }
}

function Get-OrdinalSortedStrings {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$Values
    )

    $sorted = [string[]]@($Values)
    [System.Array]::Sort($sorted, [System.StringComparer]::Ordinal)
    return $sorted
}

function Assert-ExactProperties {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Value,
        [Parameter(Mandatory = $true)]
        [string[]]$Expected,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if ($null -eq $Value -or $Value -isnot [psobject]) {
        throw "$Label must be one JSON object."
    }
    $observed = @(Get-OrdinalSortedStrings -Values @($Value.PSObject.Properties.Name))
    $wanted = @(Get-OrdinalSortedStrings -Values @($Expected))
    $difference = @(Compare-Object -ReferenceObject $wanted -DifferenceObject $observed)
    if ($difference.Count -ne 0) {
        throw "$Label does not have the exact required property set."
    }
}

function Test-IsAdditionalTeXSearchVariable {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name
    )

    $upperName = $Name.ToUpperInvariant()
    $controlledBaseNames = @('TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS')
    if ($upperName -in $controlledBaseNames) {
        return $false
    }
    $directVariables = @(
        'TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS', 'TEXFORMATS', 'TEXFONTS',
        'TEXFONTMAPS', 'TFMFONTS', 'VFFONTS', 'T1FONTS', 'AFMFONTS',
        'TTFONTS', 'OPENTYPEFONTS', 'ENCFONTS', 'CMAPFONTS', 'LIGFONTS',
        'TEXPOOL', 'MFPOOL', 'MPPOOL', 'TEXPSHEADERS', 'DVIPSHEADERS',
        'PKFONTS', 'GFONTS', 'GFFONTS', 'MISCFONTS', 'MFINPUTS',
        'MPINPUTS', 'MFBASES', 'MPMEMS', 'WEB2C', 'OFMFONTS', 'OVFFONTS',
        'MFTINPUTS', 'TEXPICTS', 'OCPINPUTS', 'OPFONTS', 'OPLFONTS',
        'OTPINPUTS', 'OVPFONTS', 'MPSUPPORT', 'TRFONTS', 'TEXCONFIG',
        'INDEXSTYLE', 'T42FONTS', 'CWEBINPUTS', 'SFDFONTS', 'LUAINPUTS',
        'CLUAINPUTS', 'OSFONTDIR', 'GLYPHLIST', 'RISRFONTS', 'TYPE1FONTS',
        'RUBYINPUTS', 'TEXDOCS', 'GLYPHFONTS', 'TEXPKS', 'TEXMFINI',
        'TEXBIB', 'VARTEXFONTS', 'TEXSOURCES', 'PSHEADERS', 'T1INPUTS',
        'TEXINDEXSTYLE', 'KPSEWHICHINPUTS', 'WEBINPUTS', 'PDFTEXCONFIG',
        'FONTFEATURES', 'FONTCIDMAPS', 'MLBIBINPUTS', 'MLBSTINPUTS',
        'RISINPUTS', 'BLTXMLINPUTS', 'MAKETEX_MODE'
    )
    foreach ($baseName in $directVariables) {
        if (
            $upperName -ceq $baseName -or
            $upperName.StartsWith("${baseName}.", [System.StringComparison]::Ordinal) -or
            $upperName.StartsWith("${baseName}_", [System.StringComparison]::Ordinal)
        ) {
            return $true
        }
    }
    if (
        $upperName.StartsWith('TEXMF', [System.StringComparison]::Ordinal) -or
        $upperName.StartsWith('KPSE_', [System.StringComparison]::Ordinal) -or
        $upperName.StartsWith('SELFAUTO', [System.StringComparison]::Ordinal)
    ) {
        return $true
    }
    return $false
}

function Write-StrictJson {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [object]$Value
    )

    $json = ConvertTo-Json -InputObject $Value -Depth 20 -Compress
    $temporary = "$Path.$PID.$([System.Guid]::NewGuid().ToString('N')).tmp"
    $backup = "$Path.$PID.$([System.Guid]::NewGuid().ToString('N')).bak"
    try {
        [System.IO.File]::WriteAllText($temporary, $json, $Utf8NoBom)
        if ([System.IO.File]::Exists($Path)) {
            [System.IO.File]::Replace($temporary, $Path, $backup, $true)
            [System.IO.File]::Delete($backup)
        }
        else {
            [System.IO.File]::Move($temporary, $Path)
        }
    }
    finally {
        if ([System.IO.File]::Exists($temporary)) {
            [System.IO.File]::Delete($temporary)
        }
        if ([System.IO.File]::Exists($backup)) {
            [System.IO.File]::Delete($backup)
        }
    }
}

function Read-StrictJsonObject {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [switch]$RequireCanonicalNoFinalLf
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "$Label was not written: $Path"
    }
    $strictJsonProgram = @'
import json
import math
import pathlib
import sys

def reject_constant(value):
    raise ValueError(f"nonfinite JSON constant {value!r} is forbidden")

def finite_float(value):
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"nonfinite JSON number {value!r} is forbidden")
    return parsed

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r} is forbidden")
        result[key] = value
    return result

raw = pathlib.Path(sys.argv[1]).read_bytes()
document = json.loads(
    raw.decode("utf-8"),
    parse_constant=reject_constant,
    parse_float=finite_float,
    object_pairs_hook=unique_object,
)
if not isinstance(document, dict):
    raise ValueError("root must be one JSON object")
canonical = json.dumps(
    document,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False,
).encode("utf-8")
sys.stdout.buffer.write(canonical + b"\n")
'@
    $encodedProgram = [System.Convert]::ToBase64String(
        [System.Text.Encoding]::UTF8.GetBytes($strictJsonProgram)
    )
    $launcher = "import base64,sys;exec(compile(base64.b64decode(sys.argv.pop(1)),'<strict-json>','exec'))"
    $invocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', '-c', $launcher, $encodedProgram, $Path
    ) -Label "$Label strict-JSON Python invocation"
    $canonical = $invocation.Output
    $parseExitCode = $invocation.ExitCode
    if ($parseExitCode -ne 0) {
        throw "$Label is not strict JSON (parser exit $parseExitCode)."
    }
    if ($RequireCanonicalNoFinalLf) {
        $rawBytes = [System.IO.File]::ReadAllBytes($Path)
        $strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
        $rawText = $strictUtf8.GetString($rawBytes)
        if ([string]$canonical -cne ($rawText + "`n")) {
            throw "$Label bytes are not canonical compact sorted strict JSON without a final LF."
        }
    }
    try {
        return ConvertFrom-Json -InputObject (@($canonical) -join "`n") -ErrorAction Stop
    }
    catch {
        throw "$Label canonical JSON could not be loaded: $($_.Exception.Message)"
    }
}

function Get-PypdfDistributionSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SiteRoot,
        [Parameter(Mandatory = $true)]
        [string]$PackageRoot,
        [Parameter(Mandatory = $true)]
        [string]$DistributionRoot,
        [Parameter(Mandatory = $true)]
        [string]$RecordPath,
        [Parameter(Mandatory = $true)]
        [string]$ModulePath
    )

    $snapshotProgram = @'
import base64
import csv
import hashlib
import json
import os
import pathlib
import re
import stat
import sys
from io import StringIO

def first_reparse(path):
    absolute = pathlib.Path(os.path.abspath(path))
    parts = absolute.parts
    current = pathlib.Path(parts[0])
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    for part in parts[1:]:
        current /= part
        information = current.lstat()
        if current.is_symlink() or bool(getattr(information, "st_file_attributes", 0) & reparse_flag):
            return current
    return None

def identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_mode,
        information.st_size,
        information.st_mtime_ns,
        information.st_ctime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

def content_identity(information):
    return [
        information.st_dev,
        information.st_ino,
        information.st_size,
        information.st_mtime_ns,
        getattr(information, "st_file_attributes", 0),
    ]

def stable_hash(path):
    mediated = first_reparse(path)
    if mediated is not None:
        raise RuntimeError(f"pypdf path is reparse-mediated at {mediated}")
    path = path.resolve(strict=True)
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise RuntimeError(f"pypdf path is not a regular file: {path}")
    digest = hashlib.sha256()
    byte_count = 0
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if content_identity(before) != content_identity(opened):
            raise RuntimeError(f"pypdf path changed while opening: {path}")
        blocks = []
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            blocks.append(block)
            byte_count += len(block)
        after_read = os.fstat(stream.fileno())
    after_close = path.lstat()
    if identity(before) != identity(after_close) or content_identity(opened) != content_identity(after_read):
        raise RuntimeError(f"pypdf path changed during stable hashing: {path}")
    return digest.hexdigest(), byte_count, b"".join(blocks)

site = pathlib.Path(sys.argv[1])
package_root = pathlib.Path(sys.argv[2])
distribution_root = pathlib.Path(sys.argv[3])
record_path = pathlib.Path(sys.argv[4])
module_path = pathlib.Path(sys.argv[5])
for path in (site, package_root, distribution_root, record_path, module_path):
    mediated = first_reparse(path)
    if mediated is not None:
        raise RuntimeError(f"fixed pypdf provenance root is reparse-mediated at {mediated}")
site = site.resolve(strict=True)
package_root = package_root.resolve(strict=True)
distribution_root = distribution_root.resolve(strict=True)
record_path = record_path.resolve(strict=True)
module_path = module_path.resolve(strict=True)
if package_root.parent != site or distribution_root.parent != site:
    raise RuntimeError("pypdf package/dist-info roots must be exact children of fixed site-packages")
if record_path != distribution_root / "RECORD" or module_path != package_root / "__init__.py":
    raise RuntimeError("pypdf RECORD/module paths do not equal the fixed distribution paths")

record_sha256, _record_size, record_bytes = stable_hash(record_path)
rows = list(csv.reader(StringIO(record_bytes.decode("utf-8"), newline="")))
if not rows:
    raise RuntimeError("pypdf RECORD is empty")
entries = []
exact_paths = set()
folded_paths = set()
resolved_paths = set()
for row_number, row in enumerate(rows, 1):
    if len(row) != 3:
        raise RuntimeError(f"pypdf RECORD row {row_number} must contain exactly three fields")
    raw_path, declared_hash, declared_size = row
    if (
        not raw_path
        or "\\" in raw_path
        or pathlib.PurePosixPath(raw_path).is_absolute()
        or any(part in {"", ".", ".."} or ":" in part for part in raw_path.split("/"))
    ):
        raise RuntimeError(f"pypdf RECORD row {row_number} has unsafe path {raw_path!r}")
    folded = raw_path.casefold()
    if raw_path in exact_paths or folded in folded_paths:
        raise RuntimeError(f"pypdf RECORD duplicate/case-collision at {raw_path!r}")
    exact_paths.add(raw_path)
    folded_paths.add(folded)
    candidate = site.joinpath(*raw_path.split("/"))
    mediated = first_reparse(candidate)
    if mediated is not None:
        raise RuntimeError(f"pypdf RECORD path is reparse-mediated at {mediated}")
    candidate = candidate.resolve(strict=True)
    try:
        candidate.relative_to(site)
    except ValueError as exc:
        raise RuntimeError(f"pypdf RECORD path escapes fixed site: {raw_path}") from exc
    normalized = os.path.normcase(str(candidate))
    if normalized in resolved_paths:
        raise RuntimeError(f"pypdf RECORD paths alias one file: {raw_path}")
    resolved_paths.add(normalized)
    actual_hash, actual_size, _payload = stable_hash(candidate)
    if bool(declared_hash) != bool(declared_size):
        raise RuntimeError(f"pypdf RECORD row {row_number} has incomplete declarations")
    if declared_hash:
        algorithm, separator, encoded = declared_hash.partition("=")
        if algorithm != "sha256" or separator != "=" or not encoded:
            raise RuntimeError(f"pypdf RECORD row {row_number} has unsupported declared hash")
        declared_bytes = base64.b64decode(
            encoded + "=" * (-len(encoded) % 4),
            altchars=b"-_",
            validate=True,
        )
        if len(declared_bytes) != hashlib.sha256().digest_size or declared_bytes.hex() != actual_hash:
            raise RuntimeError(f"pypdf RECORD declared hash disagrees for {raw_path}")
        if re.fullmatch(r"0|[1-9][0-9]*", declared_size) is None or int(declared_size) != actual_size:
            raise RuntimeError(f"pypdf RECORD declared size disagrees for {raw_path}")
    entries.append({"path": raw_path, "sha256": actual_hash, "byte_count": actual_size})
entries.sort(key=lambda entry: entry["path"])
if record_path.relative_to(site).as_posix() not in exact_paths:
    raise RuntimeError("pypdf RECORD does not inventory its own bytes")
if module_path.relative_to(site).as_posix() not in exact_paths:
    raise RuntimeError("pypdf RECORD does not inventory imported module origin")
tree_payload = json.dumps(
    entries,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
    allow_nan=False,
).encode("utf-8")
module_sha256, _module_size, _module_bytes = stable_hash(module_path)
print(
    json.dumps(
        {
            "tree_sha256": hashlib.sha256(tree_payload).hexdigest(),
            "file_count": len(entries),
            "record_sha256": record_sha256,
            "module_sha256": module_sha256,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
)
'@
    $encodedProgram = [System.Convert]::ToBase64String(
        [System.Text.Encoding]::UTF8.GetBytes($snapshotProgram)
    )
    $launcher = "import base64,sys;exec(compile(base64.b64decode(sys.argv.pop(1)),'<pypdf-snapshot>','exec'))"
    $invocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', '-c', $launcher, $encodedProgram, $SiteRoot, $PackageRoot,
        $DistributionRoot, $RecordPath, $ModulePath
    ) -Label 'pypdf distribution snapshot Python invocation'
    $output = $invocation.Output
    $exitCode = $invocation.ExitCode
    if ($exitCode -ne 0) {
        throw "Independent pypdf actual-byte snapshot failed with exit code $exitCode."
    }
    try {
        $snapshot = ConvertFrom-Json -InputObject (@($output) -join "`n") -ErrorAction Stop
    }
    catch {
        throw "Independent pypdf actual-byte snapshot is not valid JSON: $($_.Exception.Message)"
    }
    Assert-ExactProperties -Value $snapshot -Expected @(
        'tree_sha256', 'file_count', 'record_sha256', 'module_sha256'
    ) -Label 'Independent pypdf actual-byte snapshot'
    return $snapshot
}

function Assert-VerificationReport {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Report,
        [Parameter(Mandatory = $true)]
        [string]$ExpectedRevision,
        [Parameter(Mandatory = $true)]
        [string]$ExpectedResultPath,
        [Parameter(Mandatory = $true)]
        [string]$ExpectedHeadRevision,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedExecutables
    )

    Assert-ExactProperties -Value $Report -Expected @(
        'ok',
        'protocol_profile',
        'python_executable',
        'python_executable_sha256',
        'git_executable',
        'git_executable_sha256',
        'result_path',
        'source_revision',
        'head_revision',
        'input_sha256_before',
        'input_sha256_after',
        'input_unchanged',
        'semantic_payload_digest',
        'manifest_path_count',
        'check_count',
        'issues'
    ) -Label 'Verification report'
    if ([string]$Report.source_revision -cne $ExpectedRevision) {
        throw "Verification report source_revision '$($Report.source_revision)' does not equal '$ExpectedRevision'."
    }
    if ([string]$Report.head_revision -cne $ExpectedHeadRevision) {
        throw "Verification report head_revision '$($Report.head_revision)' does not equal driver M0 HEAD '$ExpectedHeadRevision'."
    }
    if ([string]$Report.protocol_profile -cne $ProductionProfile) {
        throw "Verification report protocol_profile must be exactly $ProductionProfile."
    }
    if (
        [string]$Report.python_executable -cne [string]$ExpectedExecutables.python_executable.path -or
        [string]$Report.python_executable_sha256 -cne [string]$ExpectedExecutables.python_executable.sha256 -or
        [string]$Report.git_executable -cne [string]$ExpectedExecutables.git_executable.path -or
        [string]$Report.git_executable_sha256 -cne [string]$ExpectedExecutables.git_executable.sha256
    ) {
        throw 'Verification report executable provenance does not match the trusted Python and Git bytes.'
    }
    if (
        $Report.ok -isnot [bool] -or
        $Report.ok -ne $true
    ) {
        throw 'Verification report did not report ok=true.'
    }
    if ([string]$Report.result_path -cne $ExpectedResultPath) {
        throw 'Verification report result_path does not equal VerificationResult.'
    }
    if (
        [string]$Report.input_sha256_before -cnotmatch '^[0-9a-f]{64}$' -or
        [string]$Report.input_sha256_after -cnotmatch '^[0-9a-f]{64}$' -or
        [string]$Report.input_sha256_before -cne [string]$Report.input_sha256_after -or
        $Report.input_unchanged -isnot [bool] -or
        $Report.input_unchanged -ne $true
    ) {
        throw 'Verification report does not prove an unchanged raw input identity.'
    }
    if ([string]$Report.semantic_payload_digest -cnotmatch '^[0-9a-f]{64}$') {
        throw 'Verification report has no valid semantic_payload_digest.'
    }
    if (
        $Report.manifest_path_count -isnot [int] -and
        $Report.manifest_path_count -isnot [long]
    ) {
        throw 'Verification report manifest_path_count must be an integer.'
    }
    if ([int64]$Report.manifest_path_count -lt 1) {
        throw 'Verification report manifest_path_count must be positive.'
    }
    if ($Report.check_count -isnot [int] -and $Report.check_count -isnot [long]) {
        throw 'Verification report check_count must be an integer.'
    }
    if ([int64]$Report.check_count -lt 1) {
        throw 'Verification report check_count must be positive.'
    }
    if (@($Report.issues).Count -ne 0) {
        throw 'Verification report contains issues.'
    }
}

function Assert-BuildAuditReport {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Report,
        [Parameter(Mandatory = $true)]
        [string]$ExpectedRevision,
        [Parameter(Mandatory = $true)]
        [string]$ExpectedHeadRevision,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedExecutables,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedTeXExecutables,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedBibtexStyle
    )

    Assert-ExactProperties -Value $Report -Expected @(
        'ok', 'protocol_profile', 'source_revision', 'errors', 'tool_versions',
        'inspection_tool_versions', 'commands', 'build_context', 'input_inventory',
        'source_manifest_digest', 'pdf_sha256', 'pdf_byte_count', 'page_count',
        'pdf_metadata', 'artifact_hashes', 'pages_to_render', 'changed_pages',
        'duplicate_labels', 'undefined_references', 'undefined_citations',
        'rerun_requests', 'fatal_errors', 'overfull_boxes',
        'literal_double_question_marks', 'invalid_status_tags',
        'doubled_status_tags', 'stale_auxiliary_files'
    ) -Label 'Build audit'
    if ([string]$Report.source_revision -cne $ExpectedRevision) {
        throw "Build audit source_revision '$($Report.source_revision)' does not equal '$ExpectedRevision'."
    }
    if ($Report.ok -isnot [bool] -or $Report.ok -ne $true) {
        throw 'Build audit did not report ok=true.'
    }
    if ([string]$Report.protocol_profile -cne $ProductionProfile) {
        throw "Build audit protocol_profile must be exactly $ProductionProfile."
    }
    if (
        [string]$Report.build_context.protocol_profile -cne $ProductionProfile -or
        [string]$Report.build_context.source_revision -cne $ExpectedRevision -or
        [string]$Report.build_context.head_revision -cne $ExpectedHeadRevision
    ) {
        throw 'Build audit does not carry the exact production build context.'
    }
    foreach ($field in @('python_executable', 'git_executable')) {
        $actualIdentity = $Report.build_context.$field
        $expectedIdentity = Get-PublicExecutableIdentity -Snapshot $ExpectedExecutables.$field
        Assert-ExactProperties -Value $actualIdentity -Expected @(
            'path', 'sha256', 'byte_count'
        ) -Label "Build audit build-context $field"
        if (
            [string]$actualIdentity.path -cne [string]$expectedIdentity.path -or
            [string]$actualIdentity.sha256 -cne [string]$expectedIdentity.sha256 -or
            [int64]$actualIdentity.byte_count -ne [int64]$expectedIdentity.byte_count
        ) {
            throw "Build audit build-context $field does not equal driver M0."
        }
    }
    foreach ($field in @('pdflatex_executable', 'bibtex_executable')) {
        $actualIdentity = $Report.build_context.$field
        $expectedIdentity = Get-PublicExecutableIdentity -Snapshot $ExpectedTeXExecutables.$field
        Assert-ExactProperties -Value $actualIdentity -Expected @(
            'path', 'sha256', 'byte_count'
        ) -Label "Build audit build-context $field"
        if (
            [string]$actualIdentity.path -cne [string]$expectedIdentity.path -or
            [string]$actualIdentity.sha256 -cne [string]$expectedIdentity.sha256 -or
            [int64]$actualIdentity.byte_count -ne [int64]$expectedIdentity.byte_count
        ) {
            throw "Build audit build-context $field does not equal driver M0."
        }
    }
    $actualBibtexStyle = $Report.build_context.bibtex_style
    $expectedBibtexStyleIdentity = Get-PublicExecutableIdentity -Snapshot $ExpectedBibtexStyle
    Assert-ExactProperties -Value $actualBibtexStyle -Expected @(
        'path', 'sha256', 'byte_count'
    ) -Label 'Build audit build-context bibtex_style'
    if (
        [string]$actualBibtexStyle.path -cne [string]$expectedBibtexStyleIdentity.path -or
        [string]$actualBibtexStyle.sha256 -cne [string]$expectedBibtexStyleIdentity.sha256 -or
        [int64]$actualBibtexStyle.byte_count -ne [int64]$expectedBibtexStyleIdentity.byte_count
    ) {
        throw 'Build audit build-context bibtex_style does not equal its held driver M0 identity.'
    }
    if (@($Report.commands).Count -ne 4) {
        throw 'Build audit does not contain exactly four command records.'
    }
    $expectedChildEnvironmentNames = @(
        'SystemRoot', 'WINDIR', 'SystemDrive', 'COMSPEC', 'PATHEXT', 'PATH',
        'TEMP', 'TMP', 'TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS', 'TEXMFHOME',
        'TEXMFVAR', 'TEXMFCONFIG', 'SOURCE_DATE_EPOCH'
    )
    $expectedControlledEnvironmentNames = @(
        'TEXINPUTS', 'BIBINPUTS', 'BSTINPUTS', 'TEXMFHOME', 'TEXMFVAR',
        'TEXMFCONFIG', 'SOURCE_DATE_EPOCH'
    )
    Assert-ExactProperties `
        -Value $Report.build_context.controlled_environment `
        -Expected $expectedControlledEnvironmentNames `
        -Label 'Build audit controlled environment'
    foreach ($command in @($Report.commands)) {
        Assert-ExactProperties `
            -Value $command.environment `
            -Expected $expectedChildEnvironmentNames `
            -Label 'Build audit recorded child environment'
        $expectedChildEnvironment = [ordered]@{
            SystemRoot = $WindowsDirectory
            WINDIR = $WindowsDirectory
            SystemDrive = 'C:'
            COMSPEC = Join-Path -Path $SystemDirectory -ChildPath 'cmd.exe'
            PATHEXT = '.COM;.EXE;.BAT;.CMD'
            PATH = @(
                [System.IO.Path]::GetDirectoryName([string]$command.executable),
                $SystemDirectory
            ) -join ';'
            TEMP = Join-Path -Path ([string]$Report.build_context.output_directory) -ChildPath '.tex-tmp'
            TMP = Join-Path -Path ([string]$Report.build_context.output_directory) -ChildPath '.tex-tmp'
        }
        foreach ($name in @($expectedControlledEnvironmentNames)) {
            $expectedChildEnvironment[$name] = [string]$Report.build_context.controlled_environment.$name
        }
        foreach ($name in @($expectedChildEnvironment.Keys)) {
            if ([string]$command.environment.$name -cne [string]$expectedChildEnvironment[$name]) {
                throw "Build audit recorded child environment $name is not the exact closed value."
            }
        }
        $commandTool = [System.IO.Path]::GetFileNameWithoutExtension(
            [string]$command.executable
        ).ToLowerInvariant()
        $toolField = if ($commandTool -ceq 'pdflatex') {
            'pdflatex_executable'
        }
        elseif ($commandTool -ceq 'bibtex') {
            'bibtex_executable'
        }
        else {
            throw "Build audit command uses an unexpected executable: $($command.executable)"
        }
        if ([string]$command.executable -cne [string]$Report.build_context.$toolField.path) {
            throw "Build audit command executable does not equal build-context $toolField."
        }
    }
    Assert-ExactProperties -Value $Report.inspection_tool_versions -Expected @(
        'pypdf', 'pypdf_module_path', 'pypdf_module_sha256',
        'pypdf_package_root', 'pypdf_package_tree_sha256',
        'pypdf_package_file_count', 'pypdf_distribution_root',
        'pypdf_record_path', 'pypdf_record_sha256', 'pypdf_pycache_prefix'
    ) -Label 'Build audit inspection-tool provenance'
    $pypdfVersion = [string]$Report.inspection_tool_versions.pypdf
    if ($pypdfVersion -cne $ExpectedPypdfVersion) {
        throw "Build audit pypdf version must equal the S-bound dependency pin $ExpectedPypdfVersion."
    }
    $pypdfRoot = [System.IO.Path]::GetFullPath(
        [string]$Report.inspection_tool_versions.pypdf_package_root
    )
    $pypdfPath = [System.IO.Path]::GetFullPath(
        [string]$Report.inspection_tool_versions.pypdf_module_path
    )
    $pypdfDistributionRoot = [System.IO.Path]::GetFullPath(
        [string]$Report.inspection_tool_versions.pypdf_distribution_root
    )
    $pypdfRecordPath = [System.IO.Path]::GetFullPath(
        [string]$Report.inspection_tool_versions.pypdf_record_path
    )
    $pypdfPycachePrefix = [System.IO.Path]::GetFullPath(
        [string]$Report.inspection_tool_versions.pypdf_pycache_prefix
    )
    $script:PypdfPycacheCleanupPath = $pypdfPycachePrefix
    $expectedPypdfRoot = [System.IO.Path]::GetFullPath($PypdfPackagePath)
    $expectedPypdfPath = Join-Path -Path $expectedPypdfRoot -ChildPath '__init__.py'
    $expectedDistributionRoot = Join-Path -Path $PypdfSitePath -ChildPath "pypdf-$pypdfVersion.dist-info"
    $expectedRecordPath = Join-Path -Path $expectedDistributionRoot -ChildPath 'RECORD'
    foreach ($pathAndLabel in @(
        [ordered]@{ Path = $pypdfRoot; Label = 'Build audit pypdf package root' },
        [ordered]@{ Path = $pypdfPath; Label = 'Build audit pypdf module path' },
        [ordered]@{ Path = $pypdfDistributionRoot; Label = 'Build audit pypdf dist-info root' },
        [ordered]@{ Path = $pypdfRecordPath; Label = 'Build audit pypdf RECORD path' },
        [ordered]@{ Path = $pypdfPycachePrefix; Label = 'Build audit pypdf pycache prefix' }
    )) {
        Assert-NoReparseComponents -Path $pathAndLabel.Path -Label $pathAndLabel.Label
    }
    if (
        -not $pypdfRoot.Equals($expectedPypdfRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not $pypdfPath.Equals($expectedPypdfPath, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not $pypdfDistributionRoot.Equals($expectedDistributionRoot, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not $pypdfRecordPath.Equals($expectedRecordPath, [System.StringComparison]::OrdinalIgnoreCase) -or
        -not (Test-Path -LiteralPath $pypdfRoot -PathType Container) -or
        -not (Test-Path -LiteralPath $pypdfDistributionRoot -PathType Container) -or
        -not (Test-Path -LiteralPath $pypdfPath -PathType Leaf) -or
        -not (Test-Path -LiteralPath $pypdfRecordPath -PathType Leaf)
    ) {
        throw 'Build audit pypdf module, package, dist-info, or RECORD root is not exact.'
    }
    $expectedPycacheBase = Join-Path `
        -Path ([string]$Report.build_context.output_directory) `
        -ChildPath '.tex-tmp'
    $pypdfPycacheExists = Test-Path -LiteralPath $pypdfPycachePrefix
    if (
        -not (Test-PathWithin -Candidate $pypdfPycachePrefix -Root $expectedPycacheBase) -or
        $pypdfPycachePrefix.Equals($expectedPycacheBase, [System.StringComparison]::OrdinalIgnoreCase) -or
        ($pypdfPycacheExists -and -not (Test-Path -LiteralPath $pypdfPycachePrefix -PathType Container)) -or
        ($pypdfPycacheExists -and @(Get-ChildItem -LiteralPath $pypdfPycachePrefix -Force).Count -ne 0)
    ) {
        throw 'Build audit pypdf pycache prefix is not an absent-or-empty fresh child of controlled TEMP.'
    }
    $pypdfSnapshot = Get-PypdfDistributionSnapshot `
        -SiteRoot $PypdfSitePath `
        -PackageRoot $pypdfRoot `
        -DistributionRoot $pypdfDistributionRoot `
        -RecordPath $pypdfRecordPath `
        -ModulePath $pypdfPath
    if (
        [string]$Report.inspection_tool_versions.pypdf_package_tree_sha256 -cne [string]$pypdfSnapshot.tree_sha256 -or
        [int64]$Report.inspection_tool_versions.pypdf_package_file_count -ne [int64]$pypdfSnapshot.file_count -or
        [string]$Report.inspection_tool_versions.pypdf_module_sha256 -cne [string]$pypdfSnapshot.module_sha256 -or
        [string]$Report.inspection_tool_versions.pypdf_record_sha256 -cne [string]$pypdfSnapshot.record_sha256
    ) {
        throw 'Build audit pypdf actual-byte tree digest or file identity disagrees with M1 bytes.'
    }
    $inventoryNames = @(
        Get-OrdinalSortedStrings -Values @($Report.input_inventory.PSObject.Properties.Name)
    )
    if ((@($inventoryNames) -join ',') -cne 'build,external,repository') {
        throw 'Build audit input_inventory is not the complete classified inventory.'
    }
    foreach ($category in @('repository', 'build', 'external')) {
        if (@($Report.input_inventory.$category.PSObject.Properties.Name).Count -lt 1) {
            throw "Build audit input_inventory category $category is empty."
        }
    }
    if (
        [string]$Report.pdf_sha256 -cnotmatch '^[0-9a-f]{64}$' -or
        [string]$Report.pdf_sha256 -cne [string]$Report.artifact_hashes.'main.pdf'
    ) {
        throw 'Build audit PDF identity is not bound to artifact_hashes[main.pdf].'
    }
    foreach ($field in @(
        'errors', 'duplicate_labels', 'undefined_references', 'undefined_citations',
        'rerun_requests', 'fatal_errors', 'overfull_boxes',
        'literal_double_question_marks', 'invalid_status_tags',
        'doubled_status_tags', 'stale_auxiliary_files'
    )) {
        if (@($Report.$field).Count -ne 0) {
            throw "Build audit contains findings in $field."
        }
    }
}

function Invoke-RecordedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Executable,
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [int]$Sequence,
        [Parameter(Mandatory = $true)]
        [string]$ToolVersion,
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [string]$CommandRecordPath,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [System.Collections.ArrayList]$Records,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$ControlledEnvironment,
        [Parameter(Mandatory = $true)]
        [string]$ControlledTempDirectory,
        [Parameter(Mandatory = $true)]
        [object]$ExpectedExecutableSnapshot
    )

    $executableLabel = [System.IO.Path]::GetFileName($Executable)
    $lockField = if (
        [System.IO.Path]::GetFileNameWithoutExtension($Executable).Equals(
            'pdflatex',
            [System.StringComparison]::OrdinalIgnoreCase
        )
    ) {
        'pdflatex_executable'
    }
    elseif (
        [System.IO.Path]::GetFileNameWithoutExtension($Executable).Equals(
            'bibtex',
            [System.StringComparison]::OrdinalIgnoreCase
        )
    ) {
        'bibtex_executable'
    }
    else {
        throw "Recorded command executable is not pdflatex or bibtex: $Executable"
    }
    $lockEntry = $ExecutableLaunchLocks[$lockField]
    $lockedBefore = Get-LockedExecutableSnapshot -Path $Executable -Stream $lockEntry.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $lockEntry.Snapshot `
        -Actual $lockedBefore `
        -Label $executableLabel
    $executableBefore = Get-ExternalToolRunSnapshot -Path $Executable
    Assert-ExternalToolSnapshotEqual `
        -Expected $ExpectedExecutableSnapshot `
        -Actual $executableBefore `
        -Label $executableLabel
    $stdoutPath = Join-Path -Path $BuildDirectory -ChildPath ("command-{0:d2}.stdout.txt" -f $Sequence)
    $stderrPath = Join-Path -Path $BuildDirectory -ChildPath ("command-{0:d2}.stderr.txt" -f $Sequence)
    $started = [System.DateTimeOffset]::UtcNow.ToString('o', $InvariantCulture)
    $recordedChildEnvironment = Get-ClosedChildEnvironment `
        -Executable $Executable `
        -TempDirectory $ControlledTempDirectory `
        -Additional $ControlledEnvironment
    try {
        $invocation = Invoke-ExplicitChildProcess `
            -Executable $Executable `
            -Arguments $Arguments `
            -WorkingDirectory $BuildDirectory `
            -Environment $recordedChildEnvironment
        $exitCode = $invocation.ExitCode
        [System.IO.File]::WriteAllText($stdoutPath, [string]$invocation.Output, $Utf8NoBom)
        [System.IO.File]::WriteAllText($stderrPath, [string]$invocation.Error, $Utf8NoBom)
    }
    finally {
        $executableAfter = Get-ExternalToolRunSnapshot -Path $Executable
        Assert-ExternalToolSnapshotEqual `
            -Expected $ExpectedExecutableSnapshot `
            -Actual $executableAfter `
            -Label $executableLabel
        $lockedAfter = Get-LockedExecutableSnapshot -Path $Executable -Stream $lockEntry.Stream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $lockEntry.Snapshot `
            -Actual $lockedAfter `
            -Label $executableLabel
    }
    $ended = [System.DateTimeOffset]::UtcNow.ToString('o', $InvariantCulture)

    if (-not (Test-Path -LiteralPath $stdoutPath -PathType Leaf)) {
        [System.IO.File]::WriteAllBytes($stdoutPath, [byte[]]@())
    }
    if (-not (Test-Path -LiteralPath $stderrPath -PathType Leaf)) {
        [System.IO.File]::WriteAllBytes($stderrPath, [byte[]]@())
    }
    $stdoutHash = (Get-FileHash -LiteralPath $stdoutPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $stderrHash = (Get-FileHash -LiteralPath $stderrPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $argv = @($Executable) + @($Arguments)
    $record = [ordered]@{
        argv = $argv
        returncode = [int]$exitCode
        tool_version = $ToolVersion
        executable = $Executable
        cwd = $BuildDirectory
        started_at_utc = $started
        ended_at_utc = $ended
        stdout_sha256 = $stdoutHash
        stderr_sha256 = $stderrHash
        stdout_artifact = [System.IO.Path]::GetFileName($stdoutPath)
        stderr_artifact = [System.IO.Path]::GetFileName($stderrPath)
        environment = $recordedChildEnvironment
    }
    [void]$Records.Add($record)
    Write-StrictJson -Path $CommandRecordPath -Value @($Records)

    if ($exitCode -ne 0) {
        throw "$([System.IO.Path]::GetFileName($Executable)) command $Sequence failed with exit code $exitCode."
    }
}

function New-ControlledTeXEnvironment {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [string]$SourceDateEpoch
    )

    $texmfHome = Join-Path -Path $BuildDirectory -ChildPath '.texmf-home'
    $texmfVar = Join-Path -Path $BuildDirectory -ChildPath '.texmf-var'
    $texmfConfig = Join-Path -Path $BuildDirectory -ChildPath '.texmf-config'
    $tempDirectory = Join-Path -Path $BuildDirectory -ChildPath '.tex-tmp'
    foreach ($controlledDirectory in @(
        $texmfHome,
        $texmfVar,
        $texmfConfig,
        $tempDirectory
    )) {
        [void][System.IO.Directory]::CreateDirectory($controlledDirectory)
        Assert-NoReparseComponents `
            -Path $controlledDirectory `
            -Label 'Controlled TeX user-tree root'
    }
    return [pscustomobject]@{
        Environment = [ordered]@{
            TEXINPUTS = "$SourceDirectory;$ManuscriptsDirectory;"
            BIBINPUTS = $ManuscriptsDirectory
            BSTINPUTS = [System.IO.Path]::GetDirectoryName($BibtexStylePath)
            TEXMFHOME = $texmfHome
            TEXMFVAR = $texmfVar
            TEXMFCONFIG = $texmfConfig
            SOURCE_DATE_EPOCH = $SourceDateEpoch
        }
        TempDirectory = $tempDirectory
    }
}

function Read-LockedFileBytes {
    param(
        [Parameter(Mandatory = $true)]
        [System.IO.FileStream]$Stream,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if ($Stream.Length -gt [int]::MaxValue) {
        throw "$Label exceeds the maximum supported provenance artifact size."
    }
    $bytes = [byte[]]::new([int]$Stream.Length)
    $Stream.Position = 0
    $offset = 0
    while ($offset -lt $bytes.Length) {
        $read = $Stream.Read($bytes, $offset, $bytes.Length - $offset)
        if ($read -le 0) {
            throw "$Label held handle ended before its declared length."
        }
        $offset += $read
    }
    $Stream.Position = 0
    return $bytes
}

function Assert-HeldProvenanceLockValid {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Lock,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    Assert-NoReparseComponents -Path $Lock.Path -Label $Label
    $pathNow = Get-ExternalToolRunSnapshot -Path $Lock.Path
    Assert-ExternalToolSnapshotEqual `
        -Expected $Lock.PathSnapshot `
        -Actual $pathNow `
        -Label $Label
    $lockedNow = Get-LockedExecutableSnapshot -Path $Lock.Path -Stream $Lock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $Lock.Snapshot `
        -Actual $lockedNow `
        -Label $Label
}

function Get-LockedStrictUtf8Text {
    param(
        [Parameter(Mandatory = $true)]
        [object]$Lock,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    Assert-HeldProvenanceLockValid -Lock $Lock -Label $Label
    $bytes = Read-LockedFileBytes -Stream $Lock.Stream -Label $Label
    $strictUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
    $text = $strictUtf8.GetString($bytes)
    Assert-HeldProvenanceLockValid -Lock $Lock -Label $Label
    return $text
}

function New-HeldProvenanceSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$SourcePath,
        [Parameter(Mandatory = $true)]
        [string]$SnapshotPath,
        [Parameter(Mandatory = $true)]
        [string]$Label,
        [switch]$RetainSourceLock
    )

    Assert-NoReparseComponents -Path $SourcePath -Label "$Label generated source"
    if (-not (Test-Path -LiteralPath $SourcePath -PathType Leaf)) {
        throw "$Label generated source is missing or not a regular file: $SourcePath"
    }
    if (Test-Path -LiteralPath $snapshotPath) {
        throw "$Label snapshot target already exists: $SnapshotPath"
    }
    $sourcePathSnapshot = Get-ExternalToolRunSnapshot -Path $SourcePath
    $sourceStream = Open-ExecutableLaunchLock -Path $SourcePath
    $snapshotStream = $null
    $bridgeStream = $null
    $finalSnapshotStream = $null
    try {
        $sourceLockedSnapshot = Get-LockedExecutableSnapshot `
            -Path $SourcePath `
            -Stream $sourceStream
        if (
            [string]$sourcePathSnapshot.sha256 -cne [string]$sourceLockedSnapshot.sha256 -or
            [int64]$sourcePathSnapshot.byte_count -ne [int64]$sourceLockedSnapshot.byte_count
        ) {
            throw "$Label generated source changed while its deny-write/delete handle was acquired."
        }
        $bytes = Read-LockedFileBytes -Stream $sourceStream -Label "$Label generated source"
        $sourceLockedAfterRead = Get-LockedExecutableSnapshot `
            -Path $SourcePath `
            -Stream $sourceStream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $sourceLockedSnapshot `
            -Actual $sourceLockedAfterRead `
            -Label "$Label generated source"
        $sourcePathAfterRead = Get-ExternalToolRunSnapshot -Path $SourcePath
        Assert-ExternalToolSnapshotEqual `
            -Expected $sourcePathSnapshot `
            -Actual $sourcePathAfterRead `
            -Label "$Label generated source"
        $sourceLock = [pscustomobject]@{
            Path = [System.IO.Path]::GetFullPath($SourcePath)
            Stream = $sourceStream
            Snapshot = $sourceLockedSnapshot
            PathSnapshot = $sourcePathSnapshot
        }
        Assert-HeldProvenanceLockValid `
            -Lock $sourceLock `
            -Label "$Label generated source"

        $snapshotStream = [System.IO.FileStream]::new(
            $SnapshotPath,
            [System.IO.FileMode]::CreateNew,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::Read,
            4096,
            [System.IO.FileOptions]::WriteThrough
        )
        $snapshotStream.Write($bytes, 0, $bytes.Length)
        $snapshotStream.Flush($true)
        $snapshotStream.Position = 0
        $snapshot = Get-LockedExecutableSnapshot `
            -Path $SnapshotPath `
            -Stream $snapshotStream
        if (
            [string]$snapshot.sha256 -cne [string]$sourceLockedSnapshot.sha256 -or
            [int64]$snapshot.byte_count -ne [int64]$sourceLockedSnapshot.byte_count
        ) {
            throw "$Label snapshot bytes do not equal the held generated source bytes."
        }
        $bridgeStream = [System.IO.FileStream]::new(
            $SnapshotPath,
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::Read,
            [System.IO.FileShare]::ReadWrite,
            4096,
            [System.IO.FileOptions]::RandomAccess
        )
        $bridgeSnapshot = Get-LockedExecutableSnapshot `
            -Path $SnapshotPath `
            -Stream $bridgeStream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $snapshot `
            -Actual $bridgeSnapshot `
            -Label "$Label snapshot bridge"
        $snapshotStream.Dispose()
        $snapshotStream = $null
        $finalSnapshotStream = Open-ExecutableLaunchLock -Path $SnapshotPath
        $finalSnapshot = Get-LockedExecutableSnapshot `
            -Path $SnapshotPath `
            -Stream $finalSnapshotStream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $snapshot `
            -Actual $finalSnapshot `
            -Label "$Label snapshot read-only downgrade"
        $bridgeAfterDowngrade = Get-LockedExecutableSnapshot `
            -Path $SnapshotPath `
            -Stream $bridgeStream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $snapshot `
            -Actual $bridgeAfterDowngrade `
            -Label "$Label snapshot bridge"
        $bridgeStream.Dispose()
        $bridgeStream = $null
        $lock = [pscustomobject]@{
            Path = [System.IO.Path]::GetFullPath($SnapshotPath)
            Stream = $finalSnapshotStream
            Snapshot = $finalSnapshot
            PathSnapshot = (Get-ExternalToolRunSnapshot -Path $SnapshotPath)
        }
        Assert-HeldProvenanceLockValid -Lock $lock -Label "$Label snapshot"
        $finalSnapshotStream = $null
        $retainedSourceLock = $null
        if ($RetainSourceLock) {
            $retainedSourceLock = $sourceLock
            $sourceStream = $null
        }
        return [pscustomobject]@{
            Identity = (Get-PublicExecutableIdentity -Snapshot $snapshot)
            Lock = $lock
            SourceLock = $retainedSourceLock
        }
    }
    finally {
        if ($null -ne $sourceStream) {
            $sourceStream.Dispose()
        }
        if ($null -ne $snapshotStream) {
            $snapshotStream.Dispose()
        }
        if ($null -ne $bridgeStream) {
            $bridgeStream.Dispose()
        }
        if ($null -ne $finalSnapshotStream) {
            $finalSnapshotStream.Dispose()
        }
    }
}

function Copy-RecorderSnapshot {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [ValidateSet(1, 3, 4)]
        [int]$Pass
    )

    $recorderPath = Join-Path -Path $BuildDirectory -ChildPath 'main.fls'
    $snapshotPath = Join-Path -Path $BuildDirectory -ChildPath ("main-pass-{0}.fls" -f $Pass)
    return New-HeldProvenanceSnapshot `
        -SourcePath $recorderPath `
        -SnapshotPath $snapshotPath `
        -Label "pdfTeX pass $Pass recorder"
}

function Get-BibtexInputPaths {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$DependencyLocks
    )

    $auxText = Get-LockedStrictUtf8Text `
        -Lock $DependencyLocks.aux `
        -Label 'BibTeX AUX dependency snapshot'
    $blgText = Get-LockedStrictUtf8Text `
        -Lock $DependencyLocks.blg `
        -Label 'BibTeX BLG dependency snapshot'
    $auxStyles = @(
        [regex]::Matches($auxText, '(?m)^\\bibstyle\{([^{}]+)\}\s*$') |
            ForEach-Object { [string]$_.Groups[1].Value }
    )
    $auxDatabases = @(
        [regex]::Matches($auxText, '(?m)^\\bibdata\{([^{}]+)\}\s*$') |
            ForEach-Object { [string]$_.Groups[1].Value }
    )
    if ((@($auxStyles) -join ',') -cne 'plainnat') {
        throw "main.aux must declare exactly BibTeX style plainnat; found $(@($auxStyles) -join ',')."
    }
    if ((@($auxDatabases) -join ',') -cne 'references') {
        throw "main.aux must declare exactly BibTeX database references; found $(@($auxDatabases) -join ',')."
    }
    $blgStyles = @(
        [regex]::Matches($blgText, '(?m)^The style file:\s*(.+?)\s*$') |
            ForEach-Object { [string]$_.Groups[1].Value.Trim() }
    )
    $blgDatabases = @(
        [regex]::Matches($blgText, '(?m)^Database file #\d+:\s*(.+?)\s*$') |
            ForEach-Object { [string]$_.Groups[1].Value.Trim() }
    )
    if (
        $blgStyles.Count -ne 1 -or
        [string]$blgStyles[0] -cne 'plainnat.bst'
    ) {
        throw "main.blg must record exactly the logical plainnat.bst style input; found $(@($blgStyles) -join ',')."
    }
    if (
        $blgDatabases.Count -ne 1 -or
        [string]$blgDatabases[0] -cne 'references.bib'
    ) {
        throw "main.blg must record exactly the logical references.bib database input; found $(@($blgDatabases) -join ',')."
    }
    return @($BibtexStylePath, $ReferencesBib)
}

function Add-TypedInputPath {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RawPath,
        [Parameter(Mandatory = $true)]
        [string]$RecordedWorkingDirectory,
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$Inventory,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$ResolvedPaths,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    if (-not $RawPath) {
        throw "$Label contains an empty input path."
    }
    $candidate = if ([System.IO.Path]::IsPathRooted($RawPath)) {
        [System.IO.Path]::GetFullPath($RawPath)
    }
    else {
        [System.IO.Path]::GetFullPath(
            (Join-Path -Path $RecordedWorkingDirectory -ChildPath $RawPath)
        )
    }
    Assert-NoReparseComponents -Path $candidate -Label $Label
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
        throw "$Label input is missing: $candidate"
    }
    $item = Get-Item -LiteralPath $candidate -Force -ErrorAction Stop
    if (
        $item.PSIsContainer -or
        ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0
    ) {
        throw "$Label input is not a regular non-reparse file: $candidate"
    }
    $canonical = [System.IO.Path]::GetFullPath($item.FullName)
    if (Test-PathWithin -Candidate $canonical -Root $RepositoryRoot) {
        $category = 'repository'
        $key = Get-RepositoryRelativePath -Path $canonical -RepositoryRoot $RepositoryRoot
    }
    elseif (Test-PathWithin -Candidate $canonical -Root $BuildDirectory) {
        $category = 'build'
        $key = $canonical.Substring($BuildDirectory.Length).TrimStart('\', '/').Replace('\', '/')
    }
    else {
        $category = 'external'
        $key = $canonical
    }
    $snapshot = Get-ExternalToolRunSnapshot -Path $canonical
    $identity = [ordered]@{
        sha256 = [string]$snapshot.sha256
        byte_count = [int64]$snapshot.byte_count
    }
    if ($Inventory[$category].Contains($key)) {
        $prior = $Inventory[$category][$key]
        if (
            [string]$prior.sha256 -cne [string]$identity.sha256 -or
            [int64]$prior.byte_count -ne [int64]$identity.byte_count
        ) {
            throw "$Label repeated input changed identity: $key"
        }
    }
    else {
        $Inventory[$category][$key] = $identity
        $ResolvedPaths["$category`n$key"] = $canonical
    }
    if ($category -ceq 'repository') {
        if (-not (@($RepositoryInputLocks.Keys) -ccontains $key)) {
            throw "$Label repository input is outside the prelocked verification manifest: $key"
        }
        $locked = $RepositoryInputLocks[$key]
        $lockedNow = Get-LockedExecutableSnapshot -Path $locked.Path -Stream $locked.Stream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $locked.Snapshot `
            -Actual $lockedNow `
            -Label "$Label repository input $key"
        if (
            [string]$locked.Snapshot.sha256 -cne [string]$identity.sha256 -or
            [int64]$locked.Snapshot.byte_count -ne [int64]$identity.byte_count
        ) {
            throw "$Label repository input disagrees with its prelocked identity: $key"
        }
    }
}

function Get-TypedBuildInputInventory {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$RecorderLocks,
        [Parameter(Mandatory = $true)]
        [string[]]$BibtexInputs,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [object[]]$GeneratedInputLocks,
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    $inventory = [ordered]@{
        repository = [ordered]@{}
        build = [ordered]@{}
        external = [ordered]@{}
    }
    $resolvedPaths = [ordered]@{}
    foreach ($passName in @('pass_1', 'pass_3', 'pass_4')) {
        $recorderText = Get-LockedStrictUtf8Text `
            -Lock $RecorderLocks[$passName] `
            -Label "$Label $passName recorder"
        $pwdMatches = @(
            [regex]::Matches($recorderText, '(?m)^PWD (.+)$') |
                ForEach-Object { [string]$_.Groups[1].Value.TrimEnd("`r") }
        )
        if ($pwdMatches.Count -ne 1) {
            throw "$Label $passName recorder must contain exactly one PWD record."
        }
        $recordedWorkingDirectory = [System.IO.Path]::GetFullPath($pwdMatches[0])
        if ($recordedWorkingDirectory -cne $BuildDirectory) {
            throw "$Label $passName recorder PWD does not equal its build directory."
        }
        $inputMatches = @(
            [regex]::Matches($recorderText, '(?m)^INPUT (.+)$') |
                ForEach-Object { [string]$_.Groups[1].Value.TrimEnd("`r") }
        )
        if ($inputMatches.Count -lt 1) {
            throw "$Label $passName recorder contains no INPUT records."
        }
        foreach ($inputPath in @($inputMatches)) {
            Add-TypedInputPath `
                -RawPath $inputPath `
                -RecordedWorkingDirectory $recordedWorkingDirectory `
                -BuildDirectory $BuildDirectory `
                -Inventory $inventory `
                -ResolvedPaths $resolvedPaths `
                -Label "$Label $passName recorder"
        }
    }
    foreach ($bibtexInput in @($BibtexInputs)) {
        Add-TypedInputPath `
            -RawPath $bibtexInput `
            -RecordedWorkingDirectory $BuildDirectory `
            -BuildDirectory $BuildDirectory `
            -Inventory $inventory `
            -ResolvedPaths $resolvedPaths `
            -Label "$Label BibTeX inventory"
    }
    foreach ($generatedLock in @($GeneratedInputLocks)) {
        Assert-HeldProvenanceLockValid `
            -Lock $generatedLock `
            -Label "$Label generated input $($generatedLock.Path)"
        Add-TypedInputPath `
            -RawPath $generatedLock.Path `
            -RecordedWorkingDirectory $BuildDirectory `
            -BuildDirectory $BuildDirectory `
            -Inventory $inventory `
            -ResolvedPaths $resolvedPaths `
            -Label "$Label held generated input"
        $generatedKey = [System.IO.Path]::GetFullPath($generatedLock.Path).Substring(
            $BuildDirectory.Length
        ).TrimStart('\', '/').Replace('\', '/')
        $generatedIdentity = $inventory.build[$generatedKey]
        if (
            $null -eq $generatedIdentity -or
            [string]$generatedIdentity.sha256 -cne [string]$generatedLock.Snapshot.sha256 -or
            [int64]$generatedIdentity.byte_count -ne [int64]$generatedLock.Snapshot.byte_count
        ) {
            throw "$Label held generated input identity is not authoritative: $generatedKey"
        }
    }
    $sortedInventory = [ordered]@{}
    foreach ($category in @('repository', 'build', 'external')) {
        $sortedInventory[$category] = [ordered]@{}
        foreach ($key in @(Get-OrdinalSortedStrings -Values @($inventory[$category].Keys))) {
            $sortedInventory[$category][$key] = $inventory[$category][$key]
        }
    }
    return [pscustomobject]@{
        Inventory = $sortedInventory
        ResolvedPaths = $resolvedPaths
    }
}

function Invoke-FourCommandBuildSequence {
    param(
        [Parameter(Mandatory = $true)]
        [string]$BuildDirectory,
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$ControlledEnvironment,
        [Parameter(Mandatory = $true)]
        [string]$ControlledTempDirectory,
        [Parameter(Mandatory = $true)]
        [string]$PdflatexVersion,
        [Parameter(Mandatory = $true)]
        [string]$BibtexVersion,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [System.Collections.ArrayList]$Records,
        [Parameter(Mandatory = $true)]
        [string]$CommandRecordPath
    )

    $provenanceLocks = New-Object System.Collections.ArrayList
    try {
        $pdflatexArguments = @(
            '-interaction=nonstopmode',
            '-halt-on-error',
            '-file-line-error',
            '-recorder',
            '-no-shell-escape',
            $MainTex
        )
        Invoke-RecordedCommand -Executable $PdflatexPath -Arguments $pdflatexArguments -Sequence 1 -ToolVersion $PdflatexVersion -BuildDirectory $BuildDirectory -CommandRecordPath $CommandRecordPath -Records $Records -ControlledEnvironment $ControlledEnvironment -ControlledTempDirectory $ControlledTempDirectory -ExpectedExecutableSnapshot $TeXExecutablesM0.pdflatex_executable
        $passOne = Copy-RecorderSnapshot -BuildDirectory $BuildDirectory -Pass 1
        [void]$provenanceLocks.Add($passOne.Lock)
        $bibtexAux = New-HeldProvenanceSnapshot `
            -SourcePath (Join-Path -Path $BuildDirectory -ChildPath 'main.aux') `
            -SnapshotPath (Join-Path -Path $BuildDirectory -ChildPath 'main-bibtex.aux') `
            -Label 'BibTeX AUX dependency record' `
            -RetainSourceLock
        [void]$provenanceLocks.Add($bibtexAux.Lock)
        [void]$provenanceLocks.Add($bibtexAux.SourceLock)
        Invoke-RecordedCommand -Executable $BibtexPath -Arguments @('main') -Sequence 2 -ToolVersion $BibtexVersion -BuildDirectory $BuildDirectory -CommandRecordPath $CommandRecordPath -Records $Records -ControlledEnvironment $ControlledEnvironment -ControlledTempDirectory $ControlledTempDirectory -ExpectedExecutableSnapshot $TeXExecutablesM0.bibtex_executable
        Assert-HeldProvenanceLockValid `
            -Lock $bibtexAux.SourceLock `
            -Label 'BibTeX consumed AUX dependency record'
        $bibtexBlg = New-HeldProvenanceSnapshot `
            -SourcePath (Join-Path -Path $BuildDirectory -ChildPath 'main.blg') `
            -SnapshotPath (Join-Path -Path $BuildDirectory -ChildPath 'main-bibtex.blg') `
            -Label 'BibTeX BLG dependency record'
        [void]$provenanceLocks.Add($bibtexBlg.Lock)
        $bibtexBbl = New-HeldProvenanceSnapshot `
            -SourcePath (Join-Path -Path $BuildDirectory -ChildPath 'main.bbl') `
            -SnapshotPath (Join-Path -Path $BuildDirectory -ChildPath 'main-bibtex.bbl') `
            -Label 'BibTeX generated BBL input' `
            -RetainSourceLock
        [void]$provenanceLocks.Add($bibtexBbl.Lock)
        [void]$provenanceLocks.Add($bibtexBbl.SourceLock)
        $bibtexDependencyLocks = [ordered]@{
            aux = $bibtexAux.Lock
            blg = $bibtexBlg.Lock
        }
        $bibtexInputs = [string[]]@(
            Get-BibtexInputPaths -DependencyLocks $bibtexDependencyLocks
        )
        Assert-HeldProvenanceLockValid `
            -Lock $bibtexAux.SourceLock `
            -Label 'BibTeX consumed AUX dependency record'
        $bibtexAux.SourceLock.Stream.Dispose()
        [void]$provenanceLocks.Remove($bibtexAux.SourceLock)
        Invoke-RecordedCommand -Executable $PdflatexPath -Arguments $pdflatexArguments -Sequence 3 -ToolVersion $PdflatexVersion -BuildDirectory $BuildDirectory -CommandRecordPath $CommandRecordPath -Records $Records -ControlledEnvironment $ControlledEnvironment -ControlledTempDirectory $ControlledTempDirectory -ExpectedExecutableSnapshot $TeXExecutablesM0.pdflatex_executable
        $passThree = Copy-RecorderSnapshot -BuildDirectory $BuildDirectory -Pass 3
        [void]$provenanceLocks.Add($passThree.Lock)
        Invoke-RecordedCommand -Executable $PdflatexPath -Arguments $pdflatexArguments -Sequence 4 -ToolVersion $PdflatexVersion -BuildDirectory $BuildDirectory -CommandRecordPath $CommandRecordPath -Records $Records -ControlledEnvironment $ControlledEnvironment -ControlledTempDirectory $ControlledTempDirectory -ExpectedExecutableSnapshot $TeXExecutablesM0.pdflatex_executable
        $passFour = Copy-RecorderSnapshot -BuildDirectory $BuildDirectory -Pass 4
        [void]$provenanceLocks.Add($passFour.Lock)
        return [pscustomobject]@{
            RecorderSnapshots = [ordered]@{
                pass_1 = $passOne.Identity
                pass_3 = $passThree.Identity
                pass_4 = $passFour.Identity
            }
            RecorderLocks = [ordered]@{
                pass_1 = $passOne.Lock
                pass_3 = $passThree.Lock
                pass_4 = $passFour.Lock
            }
            BibtexInputs = $bibtexInputs
            GeneratedInputLocks = [object[]]@($bibtexBbl.Lock)
            ProvenanceLocks = $provenanceLocks
        }
    }
    catch {
        foreach ($entry in @($provenanceLocks)) {
            if ($null -ne $entry.Stream) {
                $entry.Stream.Dispose()
            }
        }
        throw
    }
}

function Assert-ExternalInputLocksValid {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Label
    )

    foreach ($path in @($ExternalInputLocks.Keys)) {
        $entry = $ExternalInputLocks[$path]
        Assert-NoReparseComponents -Path $entry.Path -Label "$Label external input"
        $pathSnapshot = Get-ExternalToolRunSnapshot -Path $entry.Path
        Assert-ExternalToolSnapshotEqual `
            -Expected $entry.PathSnapshot `
            -Actual $pathSnapshot `
            -Label "$Label external input $path"
        $lockedSnapshot = Get-LockedExecutableSnapshot `
            -Path $entry.Path `
            -Stream $entry.Stream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $entry.LockedSnapshot `
            -Actual $lockedSnapshot `
            -Label "$Label external input $path"
    }
}

function Acquire-ExternalInputLocks {
    param(
        [Parameter(Mandatory = $true)]
        [System.Collections.IDictionary]$ExternalInventory
    )

    Assert-ExternalInputLocksValid -Label 'Pre-acquisition'
    $newCount = 0
    foreach ($path in @(Get-OrdinalSortedStrings -Values @($ExternalInventory.Keys))) {
        $identity = $ExternalInventory[$path]
        if (@($ExternalInputLocks.Keys) -ccontains $path) {
            $existing = $ExternalInputLocks[$path]
            if (
                [string]$existing.LockedSnapshot.sha256 -cne [string]$identity.sha256 -or
                [int64]$existing.LockedSnapshot.byte_count -ne [int64]$identity.byte_count
            ) {
                throw "Discovered external input changed identity under its retained lock: $path"
            }
            continue
        }
        Assert-NoReparseComponents -Path $path -Label 'Discovered external input'
        $stream = Open-ExecutableLaunchLock -Path $path
        $entry = [pscustomobject]@{
            Path = $path
            Stream = $stream
            LockedSnapshot = $null
            PathSnapshot = $null
        }
        $ExternalInputLocks[$path] = $entry
        $entry.LockedSnapshot = Get-LockedExecutableSnapshot -Path $path -Stream $stream
        $entry.PathSnapshot = Get-ExternalToolRunSnapshot -Path $path
        if (
            [string]$entry.LockedSnapshot.sha256 -cne [string]$identity.sha256 -or
            [int64]$entry.LockedSnapshot.byte_count -ne [int64]$identity.byte_count -or
            [string]$entry.PathSnapshot.sha256 -cne [string]$identity.sha256 -or
            [int64]$entry.PathSnapshot.byte_count -ne [int64]$identity.byte_count
        ) {
            throw "Discovered external input changed while its retained lock was acquired: $path"
        }
        $newCount++
    }
    Assert-ExternalInputLocksValid -Label 'Post-acquisition'
    return $newCount
}

function Remove-DiscoveryDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if (
        -not (Test-PathWithin -Candidate $fullPath -Root $AttestedTemporaryDirectory) -or
        $fullPath.Equals($AttestedTemporaryDirectory, [System.StringComparison]::OrdinalIgnoreCase)
    ) {
        throw "Discovery cleanup target escapes the attested temporary directory: $fullPath"
    }
    Assert-NoReparseComponents -Path $fullPath -Label 'Discovery cleanup directory'
    [System.IO.Directory]::Delete($fullPath, $true)
    if (Test-Path -LiteralPath $fullPath) {
        throw "Discovery directory still exists after cleanup: $fullPath"
    }
}

if ($SourceRevision -cnotmatch '^[0-9a-f]{40}$') {
    throw 'SourceRevision must be a full lowercase 40-hex Git commit.'
}

$InvocationDirectory = [System.IO.Path]::GetFullPath((Get-Location).Path)
foreach ($explicitPath in @(
    $RepositoryRoot,
    $SourceDirectory,
    $RepositoryBuildScript,
    $ExecutedBuildScript,
    $BootstrapAttestationPath,
    $OutputDirectory,
    $AuditPath,
    $VerificationResult,
    $VerificationReport,
    $PdflatexPath,
    $BibtexPath,
    $BibtexStylePath
)) {
    if (-not [System.IO.Path]::IsPathRooted($explicitPath)) {
        throw "Authenticated inner-build path must be explicit and absolute: $explicitPath"
    }
}
$RepositoryRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
$SourceDirectory = [System.IO.Path]::GetFullPath($SourceDirectory)
$RepositoryBuildScript = [System.IO.Path]::GetFullPath($RepositoryBuildScript)
$ExecutedBuildScript = [System.IO.Path]::GetFullPath($ExecutedBuildScript)
$BootstrapAttestationPath = [System.IO.Path]::GetFullPath($BootstrapAttestationPath)
$ManuscriptsDirectory = [System.IO.Path]::GetFullPath((Join-Path -Path $SourceDirectory -ChildPath '..'))
$MainTex = [System.IO.Path]::GetFullPath((Join-Path -Path $SourceDirectory -ChildPath 'main.tex'))
$RunChecks = [System.IO.Path]::GetFullPath((Join-Path -Path $SourceDirectory -ChildPath 'verification\run_checks.py'))
$BuildAudit = [System.IO.Path]::GetFullPath((Join-Path -Path $SourceDirectory -ChildPath 'verification\build_audit.py'))
$ReferencesBib = [System.IO.Path]::GetFullPath((Join-Path -Path $ManuscriptsDirectory -ChildPath 'references.bib'))

$OutputDirectory = [System.IO.Path]::GetFullPath($OutputDirectory)
$AuditPath = [System.IO.Path]::GetFullPath($AuditPath)
$VerificationResult = [System.IO.Path]::GetFullPath($VerificationResult)
$VerificationReport = [System.IO.Path]::GetFullPath($VerificationReport)
$PdflatexPath = [System.IO.Path]::GetFullPath($PdflatexPath)
$BibtexPath = [System.IO.Path]::GetFullPath($BibtexPath)
$BibtexStylePath = [System.IO.Path]::GetFullPath($BibtexStylePath)

$ExecutableLaunchLocks = [ordered]@{}
$RepositoryInputLocks = [ordered]@{}
$ExternalInputLocks = [ordered]@{}
$EvidenceProvenanceLocks = New-Object System.Collections.ArrayList
$VerificationResultLock = $null
$VerificationReportLock = $null
$AuditReportLock = $null
$BibtexStyleLock = $null
$RepositoryBuildScriptLock = $null
$ExecutedBuildScriptIdentity = $null
$BootstrapAttestationLock = $null
$BootstrapAttestation = $null
$AttestedTemporaryDirectory = $null
$PublishedAuditDigest = $null
$VerificationReportDigest = $null
$BuildBodyCompleted = $false
try {
Assert-NoReparseComponents -Path $RepositoryRoot -Label 'RepositoryRoot'
Assert-NoReparseComponents -Path $SourceDirectory -Label 'SourceDirectory'
Assert-NoReparseComponents -Path $OutputDirectory -Label 'OutputDirectory'
Assert-NoReparseComponents -Path $AuditPath -Label 'AuditPath'
Assert-NoReparseComponents -Path $VerificationReport -Label 'VerificationReport'
Assert-NoReparseComponents -Path $VerificationResult -Label 'VerificationResult'
Assert-NoReparseComponents -Path $RepositoryBuildScript -Label 'RepositoryBuildScript'
Assert-NoReparseComponents -Path $ExecutedBuildScript -Label 'ExecutedBuildScript'
Assert-NoReparseComponents -Path $BootstrapAttestationPath -Label 'BootstrapAttestationPath'

$expectedSourceDirectory = [System.IO.Path]::GetFullPath(
    (Join-Path -Path $RepositoryRoot -ChildPath 'manuscripts\gauge_vfe_rg')
)
$expectedRepositoryBuildScript = [System.IO.Path]::GetFullPath(
    (Join-Path -Path $expectedSourceDirectory -ChildPath 'build.ps1')
)
if ($SourceDirectory -cne $expectedSourceDirectory) {
    throw 'SourceDirectory must equal the exact gauge_vfe_rg source directory under RepositoryRoot.'
}
if ($RepositoryBuildScript -cne $expectedRepositoryBuildScript) {
    throw 'RepositoryBuildScript must equal the exact repository build.ps1 path.'
}

foreach ($identityPath in @(
    $RepositoryBuildScript,
    $ExecutedBuildScript,
    $BootstrapAttestationPath
)) {
    if (-not (Test-Path -LiteralPath $identityPath -PathType Leaf)) {
        throw "Authenticated inner-build identity input is missing: $identityPath"
    }
}

$AttestedTemporaryDirectory = [System.IO.Path]::GetFullPath(
    [System.IO.Path]::GetDirectoryName($BootstrapAttestationPath)
)
Assert-NoReparseComponents `
    -Path $AttestedTemporaryDirectory `
    -Label 'Bootstrap attested temporary-directory candidate'
if (-not (Test-Path -LiteralPath $AttestedTemporaryDirectory -PathType Container)) {
    throw 'Bootstrap attested temporary-directory candidate is not an existing directory.'
}
$PythonChildTempDirectory = $AttestedTemporaryDirectory
foreach ($entry in @(
    [ordered]@{ Field = 'python_executable'; Path = $PythonPath },
    [ordered]@{ Field = 'git_executable'; Path = $GitPath }
)) {
    Assert-NoReparseComponents -Path $entry.Path -Label 'Trusted executable'
    if (-not (Test-Path -LiteralPath $entry.Path -PathType Leaf)) {
        throw "Required trusted executable is missing: $($entry.Path)"
    }
    $stream = Open-ExecutableLaunchLock -Path $entry.Path
    $lockEntry = [pscustomobject]@{
        Stream = $stream
        Snapshot = $null
    }
    $ExecutableLaunchLocks[$entry.Field] = $lockEntry
    $lockEntry.Snapshot = Get-LockedExecutableSnapshot -Path $entry.Path -Stream $stream
}

$repositoryBuildStream = Open-ExecutableLaunchLock -Path $RepositoryBuildScript
$RepositoryBuildScriptLock = [pscustomobject]@{
    Path = $RepositoryBuildScript
    Stream = $repositoryBuildStream
    Snapshot = (Get-LockedExecutableSnapshot -Path $RepositoryBuildScript -Stream $repositoryBuildStream)
}
$attestationStream = Open-ExecutableLaunchLock -Path $BootstrapAttestationPath
$BootstrapAttestationLock = [pscustomobject]@{
    Path = $BootstrapAttestationPath
    Stream = $attestationStream
    Snapshot = (Get-LockedExecutableSnapshot -Path $BootstrapAttestationPath -Stream $attestationStream)
}
$BootstrapAttestation = Read-StrictJsonObject `
    -Path $BootstrapAttestationPath `
    -Label 'Bootstrap attestation'
Assert-ExactProperties -Value $BootstrapAttestation -Expected @(
    'protocol_profile', 'source_revision', 'repository_root', 'source_directory',
    'repository_build_script', 'executed_build_script', 'source_blob_oid',
    'source_blob_byte_count', 'source_sha256', 'bootstrap_temporary_directory',
    'bootstrap_parent_pid', 'powershell_path', 'git_path'
) -Label 'Bootstrap attestation'
if (
    [string]$BootstrapAttestation.protocol_profile -cne $ProductionProfile -or
    [string]$BootstrapAttestation.source_revision -cne $SourceRevision -or
    [string]$BootstrapAttestation.repository_root -cne $RepositoryRoot -or
    [string]$BootstrapAttestation.source_directory -cne $SourceDirectory -or
    [string]$BootstrapAttestation.repository_build_script -cne $RepositoryBuildScript -or
    [string]$BootstrapAttestation.executed_build_script -cne $ExecutedBuildScript -or
    [string]$BootstrapAttestation.powershell_path -cne $PowerShellPath -or
    [string]$BootstrapAttestation.git_path -cne $GitPath
) {
    throw 'Bootstrap attestation identity paths or source fields do not equal explicit child inputs.'
}
if (
    [string]$BootstrapAttestation.source_blob_oid -cnotmatch '^[0-9a-f]{40}$' -or
    [string]$BootstrapAttestation.source_sha256 -cnotmatch '^[0-9a-f]{64}$' -or
    ($BootstrapAttestation.source_blob_byte_count -isnot [int] -and
        $BootstrapAttestation.source_blob_byte_count -isnot [long]) -or
    [int64]$BootstrapAttestation.source_blob_byte_count -lt 1 -or
    ($BootstrapAttestation.bootstrap_parent_pid -isnot [int] -and
        $BootstrapAttestation.bootstrap_parent_pid -isnot [long]) -or
    [int64]$BootstrapAttestation.bootstrap_parent_pid -lt 1
) {
    throw 'Bootstrap attestation contains an invalid typed source identity.'
}
$AttestedTemporaryDirectory = [System.IO.Path]::GetFullPath(
    [string]$BootstrapAttestation.bootstrap_temporary_directory
)
Assert-NoReparseComponents `
    -Path $AttestedTemporaryDirectory `
    -Label 'Bootstrap attested temporary directory'
if (-not (Test-Path -LiteralPath $AttestedTemporaryDirectory -PathType Container)) {
    throw 'Bootstrap attested temporary directory is not an existing directory.'
}
if (
    $ExecutedBuildScript -cne (Join-Path -Path $AttestedTemporaryDirectory -ChildPath 'build.ps1') -or
    $BootstrapAttestationPath -cne (Join-Path -Path $AttestedTemporaryDirectory -ChildPath 'bootstrap-attestation.json')
) {
    throw 'Executed build source and attestation must be exact children of the attested temporary directory.'
}
$ExecutedBuildScriptIdentity = [ordered]@{
    path = $ExecutedBuildScript
    sha256 = [string]$BootstrapAttestation.source_sha256
    byte_count = [int64]$BootstrapAttestation.source_blob_byte_count
}
$attestationAfterRead = Get-LockedExecutableSnapshot `
    -Path $BootstrapAttestationPath `
    -Stream $BootstrapAttestationLock.Stream
Assert-LockedExecutableSnapshotEqual `
    -Expected $BootstrapAttestationLock.Snapshot `
    -Actual $attestationAfterRead `
    -Label 'Bootstrap attestation'

foreach ($requiredFile in @(
    $MainTex,
    $RunChecks,
    $BuildAudit,
    $ReferencesBib,
    $BibtexStylePath,
    $VerificationResult
)) {
    if (-not (Test-Path -LiteralPath $requiredFile -PathType Leaf)) {
        throw "Required input is missing: $requiredFile"
    }
}
Assert-NoReparseComponents -Path $BibtexStylePath -Label 'BibtexStylePath'
if ([System.IO.Path]::GetFileName($BibtexStylePath) -cne 'plainnat.bst') {
    throw 'BibtexStylePath must name exactly plainnat.bst.'
}
if (-not (Test-PathWithin -Candidate $VerificationResult -Root $RepositoryRoot)) {
    throw 'VerificationResult must be a regular file inside the repository.'
}
if (Test-PathWithin -Candidate $OutputDirectory -Root $RepositoryRoot) {
    throw 'OutputDirectory must be outside the repository source tree.'
}
foreach ($externalPath in @($AuditPath, $VerificationReport)) {
    if (Test-PathWithin -Candidate $externalPath -Root $RepositoryRoot) {
        throw "External report path must be outside the repository source tree: $externalPath"
    }
    if (Test-PathWithin -Candidate $externalPath -Root $OutputDirectory) {
        throw "External report path must be outside the build artifact hash domain: $externalPath"
    }
}
if ($AuditPath.Equals($VerificationReport, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw 'AuditPath and VerificationReport must be distinct.'
}
if ((Test-Path -LiteralPath $VerificationReport) -or (Test-Path -LiteralPath $AuditPath)) {
    throw 'VerificationReport and AuditPath must be fresh, absent external paths.'
}
if (Test-Path -LiteralPath $OutputDirectory) {
    if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
        throw "OutputDirectory exists but is not a directory: $OutputDirectory"
    }
    $existingEntries = @(Get-ChildItem -LiteralPath $OutputDirectory -Force)
    if ($existingEntries.Count -ne 0) {
        throw "OutputDirectory must be absent or empty: $OutputDirectory"
    }
}
[void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($VerificationReport))
[void][System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($AuditPath))
$CommandRecordPath = Join-Path -Path $OutputDirectory -ChildPath 'commands.json'
$BuildContextPath = Join-Path -Path $OutputDirectory -ChildPath 'build-context.json'
$PythonChildTempDirectory = $AttestedTemporaryDirectory

foreach ($trustedExecutable in @($PythonPath, $GitPath)) {
    Assert-NoReparseComponents -Path $trustedExecutable -Label 'Trusted executable'
    if (-not (Test-Path -LiteralPath $trustedExecutable -PathType Leaf)) {
        throw "Required trusted executable is missing: $trustedExecutable"
    }
}
foreach ($externalTool in @($PdflatexPath, $BibtexPath)) {
    Assert-NoReparseComponents -Path $externalTool -Label 'TeX executable'
    if (-not (Test-Path -LiteralPath $externalTool -PathType Leaf)) {
        throw "Required TeX executable is missing: $externalTool"
    }
}
foreach ($entry in @(
    [ordered]@{ Field = 'pdflatex_executable'; Path = $PdflatexPath },
    [ordered]@{ Field = 'bibtex_executable'; Path = $BibtexPath }
)) {
    $stream = Open-ExecutableLaunchLock -Path $entry.Path
    $lockEntry = [pscustomobject]@{
        Stream = $stream
        Snapshot = $null
    }
    $ExecutableLaunchLocks[$entry.Field] = $lockEntry
    $snapshot = Get-LockedExecutableSnapshot -Path $entry.Path -Stream $stream
    $lockEntry.Snapshot = $snapshot
}
$TrustedExecutablesM0 = Get-TrustedExecutableRunSnapshot
if (
    [string]$TrustedExecutablesM0.python_executable.path -cne $PythonPath -or
    [string]$TrustedExecutablesM0.git_executable.path -cne $GitPath
) {
    throw 'Trusted executable M0 paths do not equal the fixed Python and Git paths.'
}
foreach ($field in @('python_executable', 'git_executable')) {
    $pathSnapshot = $TrustedExecutablesM0.$field
    $lockedSnapshot = $ExecutableLaunchLocks[$field].Snapshot
    if (
        [string]$pathSnapshot.path -cne [string]$lockedSnapshot.path -or
        [string]$pathSnapshot.sha256 -cne [string]$lockedSnapshot.sha256 -or
        [int64]$pathSnapshot.byte_count -ne [int64]$lockedSnapshot.byte_count
    ) {
        throw "Trusted $field path snapshot does not equal its held launch-handle M0."
    }
}
$TeXExecutablesM0 = [ordered]@{
    pdflatex_executable = Get-ExternalToolRunSnapshot -Path $PdflatexPath
    bibtex_executable = Get-ExternalToolRunSnapshot -Path $BibtexPath
}
if (
    [string]$TeXExecutablesM0.pdflatex_executable.path -cne $PdflatexPath -or
    [string]$TeXExecutablesM0.bibtex_executable.path -cne $BibtexPath
) {
    throw 'TeX executable M0 paths do not equal the resolved pdflatex and bibtex paths.'
}
foreach ($field in @('pdflatex_executable', 'bibtex_executable')) {
    $pathSnapshot = $TeXExecutablesM0.$field
    $lockedSnapshot = $ExecutableLaunchLocks[$field].Snapshot
    if (
        [string]$pathSnapshot.path -cne [string]$lockedSnapshot.path -or
        [string]$pathSnapshot.sha256 -cne [string]$lockedSnapshot.sha256 -or
        [int64]$pathSnapshot.byte_count -ne [int64]$lockedSnapshot.byte_count
    ) {
        throw "TeX $field path snapshot does not equal its held launch-handle M0."
    }
}
$bibtexStyleStream = Open-ExecutableLaunchLock -Path $BibtexStylePath
$BibtexStyleLock = [pscustomobject]@{
    Path = $BibtexStylePath
    Stream = $bibtexStyleStream
    Snapshot = $null
}
$BibtexStyleLock.Snapshot = Get-LockedExecutableSnapshot `
    -Path $BibtexStylePath `
    -Stream $bibtexStyleStream
$BibtexStylePathM0 = Get-ExternalToolRunSnapshot -Path $BibtexStylePath
if (
    [string]$BibtexStylePathM0.path -cne [string]$BibtexStyleLock.Snapshot.path -or
    [string]$BibtexStylePathM0.sha256 -cne [string]$BibtexStyleLock.Snapshot.sha256 -or
    [int64]$BibtexStylePathM0.byte_count -ne [int64]$BibtexStyleLock.Snapshot.byte_count
) {
    throw 'BibTeX style path snapshot does not equal its held-handle M0.'
}

Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
$attestedBuildObjectSpec = "$($SourceRevision):manuscripts/gauge_vfe_rg/build.ps1"
$attestedBuildBlobOid = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
    'rev-parse', '--verify', $attestedBuildObjectSpec
) -Label 'Attested build source blob resolution'
$attestedBuildBlobSize = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
    'cat-file', '-s', $attestedBuildBlobOid
) -Label 'Attested build source blob size'
if (
    $attestedBuildBlobOid -cne [string]$BootstrapAttestation.source_blob_oid -or
    $attestedBuildBlobSize -cnotmatch '^[0-9]+$' -or
    [int64]$attestedBuildBlobSize -ne [int64]$BootstrapAttestation.source_blob_byte_count
) {
    throw 'Bootstrap-attested build blob identity does not equal trusted Git at SourceRevision.'
}
Assert-FileBoundToRevision `
    -Path $RepositoryBuildScript `
    -RepositoryRoot $RepositoryRoot `
    -Revision $SourceRevision
if (
    [string]$RepositoryBuildScriptLock.Snapshot.sha256 -cne
        [string]$ExecutedBuildScriptIdentity.sha256 -or
    [int64]$RepositoryBuildScriptLock.Snapshot.byte_count -ne
        [int64]$ExecutedBuildScriptIdentity.byte_count
) {
    throw 'Repository build source bytes do not equal the bootstrap-attested executed source identity.'
}
Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot

    $verificationStream = Open-ExecutableLaunchLock -Path $VerificationResult
    $VerificationResultLock = [pscustomobject]@{
        Stream = $verificationStream
        Snapshot = $null
    }
    $VerificationResultLock.Snapshot = Get-LockedExecutableSnapshot `
        -Path $VerificationResult `
        -Stream $verificationStream
    $verificationResultCandidate = Read-StrictJsonObject `
        -Path $VerificationResult `
        -Label 'Verification result candidate'
    if (
        [string]$verificationResultCandidate.protocol_profile -cne $ProductionProfile -or
        [string]$verificationResultCandidate.source_revision -cne $SourceRevision -or
        [string]$verificationResultCandidate.overall_status -cne 'PASS'
    ) {
        throw 'Verification result candidate does not carry the exact production PASS profile and source revision.'
    }
    Assert-ExactProperties -Value $verificationResultCandidate.manifest -Expected @(
        'hash_algorithm', 'hash_domain', 'path_semantics', 'bound_inputs'
    ) -Label 'Verification result candidate manifest'
    if (
        [string]$verificationResultCandidate.manifest.hash_algorithm -cne 'SHA-256' -or
        [string]$verificationResultCandidate.manifest.hash_domain -cne 'raw file bytes' -or
        [string]$verificationResultCandidate.manifest.path_semantics -cne 'repository-relative POSIX paths'
    ) {
        throw 'Verification result candidate manifest has an invalid exact envelope.'
    }
    $candidatePropertyNames = @(
        Get-OrdinalSortedStrings -Values @(
            $verificationResultCandidate.manifest.bound_inputs.PSObject.Properties.Name
        )
    )
    $candidateProperties = @(
        foreach ($name in @($candidatePropertyNames)) {
            $verificationResultCandidate.manifest.bound_inputs.PSObject.Properties[$name]
        }
    )
    if ($candidateProperties.Count -lt 1) {
        throw 'Verification result candidate manifest has no bound repository inputs.'
    }
    $foldedCandidatePaths = [System.Collections.Generic.HashSet[string]]::new(
        [System.StringComparer]::OrdinalIgnoreCase
    )
    foreach ($property in $candidateProperties) {
        $relative = [string]$property.Name
        if (
            -not $relative -or
            $relative.Contains('\') -or
            [System.IO.Path]::IsPathRooted($relative) -or
            @($relative.Split('/') | Where-Object {
                -not $_ -or $_ -ceq '.' -or $_ -ceq '..' -or $_.Contains(':')
            }).Count -ne 0
        ) {
            throw "Verification manifest contains an unsafe repository path: '$relative'."
        }
        if (-not $foldedCandidatePaths.Add($relative)) {
            throw "Verification manifest contains a case-colliding repository path: '$relative'."
        }
        Assert-ExactProperties -Value $property.Value -Expected @(
            'byte_count', 'sha256'
        ) -Label "Verification manifest entry $relative"
        if (
            [string]$property.Value.sha256 -cnotmatch '^[0-9a-f]{64}$' -or
            ($property.Value.byte_count -isnot [int] -and $property.Value.byte_count -isnot [long]) -or
            [int64]$property.Value.byte_count -lt 0
        ) {
            throw "Verification manifest entry has an invalid raw-byte identity: $relative"
        }
        $candidatePath = [System.IO.Path]::GetFullPath(
            (Join-Path -Path $RepositoryRoot -ChildPath $relative.Replace('/', '\'))
        )
        if (
            -not (Test-PathWithin -Candidate $candidatePath -Root $RepositoryRoot) -or
            -not (Test-Path -LiteralPath $candidatePath -PathType Leaf)
        ) {
            throw "Verification manifest entry is not a regular repository file: $relative"
        }
        Assert-NoReparseComponents -Path $candidatePath -Label "Verification manifest entry $relative"
        $stream = Open-ExecutableLaunchLock -Path $candidatePath
        $inputLock = [pscustomobject]@{
            Path = $candidatePath
            Stream = $stream
            Snapshot = $null
        }
        $RepositoryInputLocks[$relative] = $inputLock
        $inputLock.Snapshot = Get-LockedExecutableSnapshot -Path $candidatePath -Stream $stream
        if (
            [string]$inputLock.Snapshot.sha256 -cne [string]$property.Value.sha256 -or
            [int64]$inputLock.Snapshot.byte_count -ne [int64]$property.Value.byte_count
        ) {
            throw "Verification manifest entry disagrees with held-handle M0 bytes: $relative"
        }
    }
    foreach ($requiredInput in @(
        $RepositoryBuildScript, $MainTex, $RunChecks, $BuildAudit, $ReferencesBib
    )) {
        $requiredRelative = Get-RepositoryRelativePath `
            -Path $requiredInput `
            -RepositoryRoot $RepositoryRoot
        if (-not (@($RepositoryInputLocks.Keys) -ccontains $requiredRelative)) {
            throw "Verification manifest omits required build input: $requiredRelative"
        }
    }

    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $resolvedSourceRevision = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'rev-parse', '--verify', "${SourceRevision}^{commit}"
    ) -Label 'Source revision resolution'
    if ($resolvedSourceRevision -cne $SourceRevision) {
        throw "SourceRevision resolved to unexpected commit '$resolvedSourceRevision'."
    }
    $HeadRevision = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'rev-parse', '--verify', 'HEAD^{commit}'
    ) -Label 'HEAD resolution'
    if ($HeadRevision -cnotmatch '^[0-9a-f]{40}$') {
        throw "Trusted Git returned an invalid HEAD revision: '$HeadRevision'."
    }
    [void](Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'merge-base', '--is-ancestor', $SourceRevision, $HeadRevision
    ) -Label 'SourceRevision ancestry check')
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot

    foreach ($relative in @($RepositoryInputLocks.Keys)) {
        Assert-FileBoundToRevision `
            -Path $RepositoryInputLocks[$relative].Path `
            -RepositoryRoot $RepositoryRoot `
            -Revision $SourceRevision
    }
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot

    $sourceDateEpoch = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'show', '-s', '--format=%ct', $SourceRevision
    ) -Label 'SOURCE_DATE_EPOCH derivation'
    if ($sourceDateEpoch -cnotmatch '^[0-9]+$') {
        throw "Git returned an invalid SOURCE_DATE_EPOCH value: '$sourceDateEpoch'."
    }
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $PythonChildAdditionalEnvironment = [ordered]@{
        SOURCE_DATE_EPOCH = $sourceDateEpoch
    }
    $lockedRepositoryInputs = [ordered]@{}
    foreach ($relative in @(Get-OrdinalSortedStrings -Values @($RepositoryInputLocks.Keys))) {
        $snapshot = $RepositoryInputLocks[$relative].Snapshot
        $lockedRepositoryInputs[$relative] = [ordered]@{
            sha256 = [string]$snapshot.sha256
            byte_count = [int64]$snapshot.byte_count
        }
    }

    $verificationInvocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', $RunChecks, '--verify', $VerificationResult, '--report', $VerificationReport
    ) -Label 'Numerical verifier Python invocation'
    $verificationExitCode = $verificationInvocation.ExitCode
    if (-not (Test-Path -LiteralPath $VerificationReport -PathType Leaf)) {
        throw 'Numerical verifier did not publish VerificationReport.'
    }
    $verificationReportStream = Open-ExecutableLaunchLock -Path $VerificationReport
    $VerificationReportLock = [pscustomobject]@{
        Path = $VerificationReport
        Stream = $verificationReportStream
        Snapshot = (Get-LockedExecutableSnapshot -Path $VerificationReport -Stream $verificationReportStream)
    }
    $verificationReportBytes = [System.IO.File]::ReadAllBytes($VerificationReport)
    $strictVerificationUtf8 = New-Object System.Text.UTF8Encoding($false, $true)
    $verificationReportText = $strictVerificationUtf8.GetString($verificationReportBytes)
    if (
        ($verificationReportBytes.Length -ge 3 -and
            $verificationReportBytes[0] -eq 0xEF -and
            $verificationReportBytes[1] -eq 0xBB -and
            $verificationReportBytes[2] -eq 0xBF) -or
        $verificationReportText.Contains("`r") -or
        $verificationReportText.Contains("`n")
    ) {
        throw 'VerificationReport must be canonical strict UTF-8 JSON without BOM, CR, or LF.'
    }
    if ([string]$verificationInvocation.Output -cne ($verificationReportText + "`n")) {
        throw 'Verification report stdout does not equal retained VerificationReport bytes.'
    }
    $verificationReportLockedAfterRead = Get-LockedExecutableSnapshot `
        -Path $VerificationReport `
        -Stream $VerificationReportLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $VerificationReportLock.Snapshot `
        -Actual $verificationReportLockedAfterRead `
        -Label 'VerificationReport publication'
    $VerificationReportDigest = [string]$VerificationReportLock.Snapshot.sha256
    $verificationDocument = Read-StrictJsonObject `
        -Path $VerificationReport `
        -Label 'Verification report' `
        -RequireCanonicalNoFinalLf
    Assert-VerificationReport -Report $verificationDocument -ExpectedRevision $SourceRevision -ExpectedResultPath $VerificationResult -ExpectedHeadRevision $HeadRevision -ExpectedExecutables $TrustedExecutablesM0
    if ($verificationExitCode -ne 0) {
        throw "Numerical verification process failed with exit code $verificationExitCode despite its report."
    }
    $verificationResultDocument = Read-StrictJsonObject -Path $VerificationResult -Label 'Verification result'
    if (
        [string]$verificationResultDocument.protocol_profile -cne $ProductionProfile -or
        [string]$verificationResultDocument.source_revision -cne $SourceRevision -or
        [string]$verificationResultDocument.overall_status -cne 'PASS'
    ) {
        throw 'Verification result does not carry the exact production PASS profile and source revision.'
    }

    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    foreach ($boundPath in @($RepositoryBuildScript, $RunChecks, $BuildAudit)) {
        Assert-FileBoundToRevision -Path $boundPath -RepositoryRoot $RepositoryRoot -Revision $SourceRevision
    }
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot

    $pdflatexVersion = Get-ToolIdentity -Executable $PdflatexPath -ExpectedSnapshot $TeXExecutablesM0.pdflatex_executable
    $bibtexVersion = Get-ToolIdentity -Executable $BibtexPath -ExpectedSnapshot $TeXExecutablesM0.bibtex_executable

    $convergedIteration = $null
    for ($iteration = 1; $iteration -le $ExternalInputDiscoveryLimit; $iteration++) {
        Assert-ExternalInputLocksValid -Label "Discovery iteration $iteration preflight"
        $discoveryDirectory = Join-Path `
            -Path $AttestedTemporaryDirectory `
            -ChildPath ("gauge-vfe-discovery-{0:d2}-{1}" -f $iteration, [guid]::NewGuid().ToString('N'))
        if (Test-Path -LiteralPath $discoveryDirectory) {
            throw "Fresh discovery directory unexpectedly exists: $discoveryDirectory"
        }
        [void][System.IO.Directory]::CreateDirectory($discoveryDirectory)
        Assert-NoReparseComponents -Path $discoveryDirectory -Label 'Fresh discovery directory'
        $discoverySequence = $null
        try {
            if (@(Get-ChildItem -LiteralPath $discoveryDirectory -Force).Count -ne 0) {
                throw 'Fresh discovery directory is not empty.'
            }
            $discoveryControl = New-ControlledTeXEnvironment `
                -BuildDirectory $discoveryDirectory `
                -SourceDateEpoch $sourceDateEpoch
            $discoveryRecords = New-Object System.Collections.ArrayList
            $discoveryCommandRecord = Join-Path -Path $discoveryDirectory -ChildPath 'commands.json'
            $discoverySequence = Invoke-FourCommandBuildSequence `
                -BuildDirectory $discoveryDirectory `
                -ControlledEnvironment $discoveryControl.Environment `
                -ControlledTempDirectory $discoveryControl.TempDirectory `
                -PdflatexVersion $pdflatexVersion `
                -BibtexVersion $bibtexVersion `
                -Records $discoveryRecords `
                -CommandRecordPath $discoveryCommandRecord
            $discoveryInventory = Get-TypedBuildInputInventory `
                -RecorderLocks $discoverySequence.RecorderLocks `
                -BibtexInputs $discoverySequence.BibtexInputs `
                -GeneratedInputLocks $discoverySequence.GeneratedInputLocks `
                -BuildDirectory $discoveryDirectory `
                -Label "Discovery iteration $iteration"
            $priorExternalPaths = @(
                Get-OrdinalSortedStrings -Values @($ExternalInputLocks.Keys)
            )
            $iterationExternalPaths = @(
                Get-OrdinalSortedStrings -Values @($discoveryInventory.Inventory.external.Keys)
            )
            $iterationEqualsPriorLocks = (
                (@($priorExternalPaths) -join "`n") -ceq
                (@($iterationExternalPaths) -join "`n")
            )
            [void](Acquire-ExternalInputLocks `
                -ExternalInventory $discoveryInventory.Inventory.external)
            if ($iterationEqualsPriorLocks) {
                $convergedIteration = $iteration
            }
        }
        finally {
            if ($null -ne $discoverySequence) {
                foreach ($entry in @($discoverySequence.ProvenanceLocks)) {
                    if ($null -ne $entry.Stream) {
                        $entry.Stream.Dispose()
                    }
                }
            }
            Remove-DiscoveryDirectory -Path $discoveryDirectory
        }
        if ($null -ne $convergedIteration) {
            break
        }
    }
    if ($null -eq $convergedIteration) {
        throw "External input discovery did not converge within $ExternalInputDiscoveryLimit iterations."
    }
    Assert-ExternalInputLocksValid -Label 'Fixed-point closure'

    if (Test-Path -LiteralPath $OutputDirectory) {
        if (-not (Test-Path -LiteralPath $OutputDirectory -PathType Container)) {
            throw "OutputDirectory changed into a non-directory before evidence: $OutputDirectory"
        }
        if (@(Get-ChildItem -LiteralPath $OutputDirectory -Force).Count -ne 0) {
            throw 'OutputDirectory was not fresh and empty when evidence began.'
        }
    }
    else {
        [void][System.IO.Directory]::CreateDirectory($OutputDirectory)
    }
    Assert-NoReparseComponents -Path $OutputDirectory -Label 'Fresh evidence OutputDirectory'
    $evidenceControl = New-ControlledTeXEnvironment `
        -BuildDirectory $OutputDirectory `
        -SourceDateEpoch $sourceDateEpoch
    $controlledTeXChildEnvironment = $evidenceControl.Environment
    $controlledTempDirectory = $evidenceControl.TempDirectory
    $PythonChildTempDirectory = $controlledTempDirectory
    $records = New-Object System.Collections.ArrayList
    $evidenceSequence = Invoke-FourCommandBuildSequence `
        -BuildDirectory $OutputDirectory `
        -ControlledEnvironment $controlledTeXChildEnvironment `
        -ControlledTempDirectory $controlledTempDirectory `
        -PdflatexVersion $pdflatexVersion `
        -BibtexVersion $bibtexVersion `
        -Records $records `
        -CommandRecordPath $CommandRecordPath
    foreach ($entry in @($evidenceSequence.ProvenanceLocks)) {
        [void]$EvidenceProvenanceLocks.Add($entry)
    }
    $evidenceInventory = Get-TypedBuildInputInventory `
        -RecorderLocks $evidenceSequence.RecorderLocks `
        -BibtexInputs $evidenceSequence.BibtexInputs `
        -GeneratedInputLocks $evidenceSequence.GeneratedInputLocks `
        -BuildDirectory $OutputDirectory `
        -Label 'Evidence build'
    Assert-ExternalInputLocksValid -Label 'Evidence inventory closure'
    foreach ($path in @($evidenceInventory.Inventory.external.Keys)) {
        if (-not (@($ExternalInputLocks.Keys) -ccontains $path)) {
            throw "Evidence external input is outside the locked fixed-point envelope: $path"
        }
        $locked = $ExternalInputLocks[$path].LockedSnapshot
        $evidenceIdentity = $evidenceInventory.Inventory.external[$path]
        if (
            [string]$locked.sha256 -cne [string]$evidenceIdentity.sha256 -or
            [int64]$locked.byte_count -ne [int64]$evidenceIdentity.byte_count
        ) {
            throw "Evidence external input changed from its locked fixed-point identity: $path"
        }
    }

    $fixedPointInputs = [ordered]@{}
    foreach ($path in @(Get-OrdinalSortedStrings -Values @($ExternalInputLocks.Keys))) {
        $snapshot = $ExternalInputLocks[$path].LockedSnapshot
        $fixedPointInputs[$path] = [ordered]@{
            sha256 = [string]$snapshot.sha256
            byte_count = [int64]$snapshot.byte_count
        }
    }
    $buildContext = [ordered]@{
        protocol_profile = $ProductionProfile
        source_revision = $SourceRevision
        head_revision = $HeadRevision
        repository_root = $RepositoryRoot
        source_directory = $SourceDirectory
        output_directory = $OutputDirectory
        initial_entries = @()
        source_date_epoch = $sourceDateEpoch
        controlled_environment = $controlledTeXChildEnvironment
        locked_repository_inputs = $lockedRepositoryInputs
        python_executable = Get-PublicExecutableIdentity -Snapshot $TrustedExecutablesM0.python_executable
        git_executable = Get-PublicExecutableIdentity -Snapshot $TrustedExecutablesM0.git_executable
        pdflatex_executable = Get-PublicExecutableIdentity -Snapshot $TeXExecutablesM0.pdflatex_executable
        bibtex_executable = Get-PublicExecutableIdentity -Snapshot $TeXExecutablesM0.bibtex_executable
        build_script = Get-FileIdentityRecord -Path $RepositoryBuildScript -RepositoryRoot $RepositoryRoot
        repository_build_script = Get-PublicExecutableIdentity -Snapshot $RepositoryBuildScriptLock.Snapshot
        executed_build_script = $ExecutedBuildScriptIdentity
        bootstrap_attestation = Get-PublicExecutableIdentity -Snapshot $BootstrapAttestationLock.Snapshot
        main_tex = Get-FileIdentityRecord -Path $MainTex -RepositoryRoot $RepositoryRoot
        run_checks = Get-FileIdentityRecord -Path $RunChecks -RepositoryRoot $RepositoryRoot
        build_audit = Get-FileIdentityRecord -Path $BuildAudit -RepositoryRoot $RepositoryRoot
        references_bib = Get-FileIdentityRecord -Path $ReferencesBib -RepositoryRoot $RepositoryRoot
        bibtex_style = Get-PublicExecutableIdentity -Snapshot $BibtexStylePathM0
        verification_result = Get-FileIdentityRecord -Path $VerificationResult -RepositoryRoot $RepositoryRoot
        external_input_fixed_point = [ordered]@{
            max_iterations = [int]$ExternalInputDiscoveryLimit
            converged_iteration = [int]$convergedIteration
            inputs = $fixedPointInputs
        }
        recorder_snapshots = $evidenceSequence.RecorderSnapshots
        evidence_input_inventory = $evidenceInventory.Inventory
    }
    Write-StrictJson -Path $BuildContextPath -Value $buildContext
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    Assert-FileBoundToRevision -Path $BuildAudit -RepositoryRoot $RepositoryRoot -Revision $SourceRevision
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $auditInvocation = Invoke-TrustedPythonCapture -Arguments @(
        '-I', '-S', $BuildAudit, '--repo-root', $RepositoryRoot, '--build-dir',
        $OutputDirectory, '--source-revision', $SourceRevision, '--command-record',
        $CommandRecordPath, '--output', $AuditPath
    ) -Label 'Build auditor Python invocation'
    $auditExitCode = $auditInvocation.ExitCode
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    if (-not (Test-Path -LiteralPath $AuditPath -PathType Leaf)) {
        throw 'Build auditor did not publish AuditPath.'
    }
    $auditStdout = [string]$auditInvocation.Output
    if ($auditStdout -cnotmatch '^BUILD_AUDIT_SHA256=([0-9a-f]{64})\n$') {
        throw 'Build auditor stdout was not the exact authenticated audit digest marker.'
    }
    $publishedAuditDigestFromChild = [string]$Matches[1]
    $auditReportStream = Open-ExecutableLaunchLock -Path $AuditPath
    $AuditReportLock = [pscustomobject]@{
        Path = $AuditPath
        Stream = $auditReportStream
        Snapshot = (Get-LockedExecutableSnapshot -Path $AuditPath -Stream $auditReportStream)
    }
    if ($publishedAuditDigestFromChild -cne [string]$AuditReportLock.Snapshot.sha256) {
        throw 'Published build audit digest does not equal retained AuditPath bytes.'
    }
    $auditReportLockedAfterPublication = Get-LockedExecutableSnapshot `
        -Path $AuditPath `
        -Stream $AuditReportLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $AuditReportLock.Snapshot `
        -Actual $auditReportLockedAfterPublication `
        -Label 'Build audit publication'
    $PublishedAuditDigest = [string]$AuditReportLock.Snapshot.sha256
    $auditDocument = Read-StrictJsonObject -Path $AuditPath -Label 'Build audit'
    Assert-BuildAuditReport -Report $auditDocument -ExpectedRevision $SourceRevision -ExpectedHeadRevision $HeadRevision -ExpectedExecutables $TrustedExecutablesM0 -ExpectedTeXExecutables $TeXExecutablesM0 -ExpectedBibtexStyle $BibtexStyleLock.Snapshot
    if ($auditExitCode -ne 0) {
        throw "Build audit process failed with exit code $auditExitCode despite its report."
    }
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $FinalHeadRevision = Invoke-TrustedGit -RepositoryRoot $RepositoryRoot -Arguments @(
        'rev-parse', '--verify', 'HEAD^{commit}'
    ) -Label 'Final HEAD resolution'
    if ($FinalHeadRevision -cne $HeadRevision) {
        throw "Current Git HEAD changed during the build handoff: '$HeadRevision' -> '$FinalHeadRevision'."
    }
    Assert-NoGitMetadataOverrides -RepositoryRoot $RepositoryRoot
    $TrustedExecutablesM1 = Get-TrustedExecutableRunSnapshot
    Assert-TrustedExecutableSnapshotsEqual -Before $TrustedExecutablesM0 -After $TrustedExecutablesM1
    $PdflatexExecutableM1 = Get-ExternalToolRunSnapshot -Path $PdflatexPath
    Assert-ExternalToolSnapshotEqual -Expected $TeXExecutablesM0.pdflatex_executable -Actual $PdflatexExecutableM1 -Label 'pdflatex executable'
    $BibtexExecutableM1 = Get-ExternalToolRunSnapshot -Path $BibtexPath
    Assert-ExternalToolSnapshotEqual -Expected $TeXExecutablesM0.bibtex_executable -Actual $BibtexExecutableM1 -Label 'bibtex executable'
    $BibtexStylePathM1 = Get-ExternalToolRunSnapshot -Path $BibtexStylePath
    Assert-ExternalToolSnapshotEqual -Expected $BibtexStylePathM0 -Actual $BibtexStylePathM1 -Label 'BibTeX style input'
    $BibtexStyleLockedM1 = Get-LockedExecutableSnapshot `
        -Path $BibtexStylePath `
        -Stream $BibtexStyleLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $BibtexStyleLock.Snapshot `
        -Actual $BibtexStyleLockedM1 `
        -Label 'BibTeX style input'
    foreach ($relative in @($RepositoryInputLocks.Keys)) {
        $inputLock = $RepositoryInputLocks[$relative]
        $lockedM1 = Get-LockedExecutableSnapshot -Path $inputLock.Path -Stream $inputLock.Stream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $inputLock.Snapshot `
            -Actual $lockedM1 `
            -Label "Repository input $relative"
    }
    $verificationResultM1 = Get-LockedExecutableSnapshot `
        -Path $VerificationResult `
        -Stream $VerificationResultLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $VerificationResultLock.Snapshot `
        -Actual $verificationResultM1 `
        -Label 'Verification result evidence'
    $verificationReportM1 = Get-LockedExecutableSnapshot `
        -Path $VerificationReportLock.Path `
        -Stream $VerificationReportLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $VerificationReportLock.Snapshot `
        -Actual $verificationReportM1 `
        -Label 'Verification report evidence'
    $auditReportM1 = Get-LockedExecutableSnapshot `
        -Path $AuditReportLock.Path `
        -Stream $AuditReportLock.Stream
    Assert-LockedExecutableSnapshotEqual `
        -Expected $AuditReportLock.Snapshot `
        -Actual $auditReportM1 `
        -Label 'Build audit evidence'
    Assert-ExternalInputLocksValid -Label 'Final external input lock validation'
    foreach ($entry in @($EvidenceProvenanceLocks)) {
        Assert-HeldProvenanceLockValid `
            -Lock $entry `
            -Label "Evidence provenance $($entry.Path)"
    }
    foreach ($identityLock in @(
        $RepositoryBuildScriptLock,
        $BootstrapAttestationLock
    )) {
        $identityM1 = Get-LockedExecutableSnapshot `
            -Path $identityLock.Path `
            -Stream $identityLock.Stream
        Assert-LockedExecutableSnapshotEqual `
            -Expected $identityLock.Snapshot `
            -Actual $identityM1 `
            -Label "Authenticated identity $($identityLock.Path)"
    }
    [Console]::Out.Write("BUILD_AUDIT_SHA256=$PublishedAuditDigest`n")
    [Console]::Out.Write("BUILD_VERIFICATION_REPORT_SHA256=$VerificationReportDigest`n")
    $BuildBodyCompleted = $true
}
finally {
    $cleanupFailures = New-Object System.Collections.ArrayList
    if ($null -ne $PypdfPycacheCleanupPath -and (Test-Path -LiteralPath $PypdfPycacheCleanupPath)) {
        try {
            Assert-NoReparseComponents `
                -Path $PypdfPycacheCleanupPath `
                -Label 'Build audit pypdf pycache cleanup root'
            if (@(Get-ChildItem -LiteralPath $PypdfPycacheCleanupPath -Force).Count -ne 0) {
                throw 'Build audit pypdf pycache cleanup root is unexpectedly nonempty.'
            }
            [System.IO.Directory]::Delete($PypdfPycacheCleanupPath, $false)
        }
        catch {
            [void]$cleanupFailures.Add("Build audit pypdf pycache cleanup failed: $($_.Exception.Message)")
        }
    }
    if ($null -ne $BibtexStyleLock -and $null -ne $BibtexStyleLock.Stream) {
        try {
            $BibtexStyleLock.Stream.Dispose()
        }
        catch {
            [void]$cleanupFailures.Add("BibTeX style lock disposal failed: $($_.Exception.Message)")
        }
    }
    foreach ($entry in @($RepositoryInputLocks.Values)) {
        if ($null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("Repository input lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    foreach ($entry in @(
        $RepositoryBuildScriptLock,
        $BootstrapAttestationLock
    )) {
        if ($null -ne $entry -and $null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("Authenticated identity lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    if ($null -ne $VerificationResultLock -and $null -ne $VerificationResultLock.Stream) {
        try {
            $VerificationResultLock.Stream.Dispose()
        }
        catch {
            [void]$cleanupFailures.Add("Verification result lock disposal failed: $($_.Exception.Message)")
        }
    }
    foreach ($entry in @($VerificationReportLock, $AuditReportLock)) {
        if ($null -ne $entry -and $null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("Published report lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    foreach ($entry in @($ExternalInputLocks.Values)) {
        if ($null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("External input lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    foreach ($entry in @($EvidenceProvenanceLocks)) {
        if ($null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("Evidence provenance lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    foreach ($entry in @($ExecutableLaunchLocks.Values)) {
        if ($null -ne $entry.Stream) {
            try {
                $entry.Stream.Dispose()
            }
            catch {
                [void]$cleanupFailures.Add("Executable launch-lock disposal failed: $($_.Exception.Message)")
            }
        }
    }
    if ($cleanupFailures.Count -ne 0) {
        $cleanupMessage = @($cleanupFailures) -join '; '
        if ($BuildBodyCompleted) {
            throw $cleanupMessage
        }
        [Console]::Error.WriteLine("Cleanup diagnostics after primary failure: $cleanupMessage")
    }
}
