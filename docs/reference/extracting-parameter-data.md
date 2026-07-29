# Extracting Access's own parameter data

The Virus TI Software Suite installer ships **Access's own parameter model** —
`remotedevice.xml` — listing every parameter the Virus Control editor knows
about, with its SysEx **bank**, **index**, range, default and value list.

This is a **cross-checking and gap-finding aid, not a source of truth for this
repo.** Everything documented here is still expected to be confirmed against
hardware per
[hardware-mapping-workflow](../../.cursor/skills/hardware-mapping-workflow/SKILL.md);
what the XML gives you is a complete list of *what to go and test*, and the
manufacturer's own name for each control.

No file from the installer is redistributed here — these are instructions for
extracting it from a copy you already have.

## Contents

* [What is in it](#what-is-in-it)
* [macOS](#macos)
* [Windows](#windows)
* [Linux](#linux)
* [Reading it](#reading-it)
* [The one format trap](#the-one-format-trap)
* [Verified on](#verified-on)

---

## What is in it

Seven XML resources ship in every suite. `PR` denotes the **Snow** variant; the
unsuffixed name is `Virus TI Desktop/Polar/Keyboard`.

| File                 | Contents                                                          |
| -------------------- | ----------------------------------------------------------------- |
| `remotedevice.xml`   | **Parameter model** — bank, index, min/max, default, value list   |
| `remotedevicePR.xml` | Same, for the Snow                                                |
| `editor.xml`         | GUI layout — *not* the parameter table, despite a similar size    |
| `editorPR.xml`       | Snow GUI layout                                                   |
| `editordevice.xml`   | A smaller, older `Remotedevice` (self-dated `4.0.0.08`)           |
| `automation.xml`     | Automation slot map                                               |
| `automationPR.xml`   | Snow automation slot map                                          |

Parameter counts in `remotedevice.xml` from the 5.1.7.00 suite, by SysEx bank:

| Bank   | Page in [address-index.md](address-index.md) | Parameters |
| ------ | -------------------------------------------- | ---------- |
| `0x6E` | Part buffer                                  | 84         |
| `0x6F` | Extended                                     | 103        |
| `0x70` | Page A                                       | 151        |
| `0x71` | Page B                                       | 114        |
| `0x72` | Multi / common                               | 32         |
| `0x73` | Global / CONFIG                              | 84         |
| `0x74` | *(not yet documented in this repo)*          | 19         |

The XML carries its own build tag, which is **older than the installer's**
version — 5.1.7.00 (2017) ships an XML stamped `version="7.2 111"`,
`releasedate="15.05.2012"`. Do not assume "latest installer" means "latest
parameter model".

## macOS

Everything needed is preinstalled.

```bash
mkdir -p ~/virus-xml && cd ~/virus-xml
pkgutil --expand-full "/path/to/Virus TI Software Suite 5.1.7.00.pkg" expanded
find expanded -name 'remotedevice*.xml' -exec cp {} . \;
```

The file lands under
`expanded/Core_components.pkg/Payload/Library/Application Support/Access Music/`
`Virus TI/Common/Virus Control.bundle/Contents/Resources/`. The target directory
must not already exist.

A manual equivalent, if `pkgutil` gives trouble:

```bash
xar -xf "/path/to/Virus TI Software Suite 5.1.7.00.pkg"
gunzip -dc Core_components.pkg/Payload | cpio -idmu
find . -name 'remotedevice*.xml'
```

## Windows

**On Windows the XML is not a file.** Unpacking the `.msi` yields 146 files and
no `.xml` at all — the XMLs are Win32 **resources** embedded inside
`Virus Control.dll`. This is the step that makes the Windows route look like a
dead end. Two steps, and [7-Zip](https://www.7-zip.org/) is the only tool
needed.

Unpack the MSI (administrative install — extracts without installing):

```bat
mkdir C:\virus-msi
msiexec /a "C:\path\to\Virus TI Software Suite 5.1.7.00.msi" /qb TARGETDIR=C:\virus-msi
```

Then pull the resources out of the DLL. 7-Zip can open a PE binary and browse
its resource section:

```bat
"C:\Program Files\7-Zip\7z.exe" e -oC:\virus-xml ^
  "C:\virus-msi\Program Files\Access Music\Virus TI\Common\Virus Control.dll" ^
  ".rsrc/0/XML/*" -y
```

In the GUI: right-click `Virus Control.dll` → **7-Zip → Open archive**, browse
to `.rsrc\0\XML\`, drag out `REMOTEDEVICE.XML`. Extracted names are upper-case;
the bytes are identical to the macOS file's. Both the 32-bit and 64-bit MSIs
work.

## Linux

The `.msi` route needs only packaged tools:

```bash
sudo apt install msitools p7zip-full

msiextract -C ~/virus-msi "Virus TI Software Suite 5.1.7.00.msi"
7z e -o ~/virus-xml "$HOME/virus-msi/Program Files/Access Music/Virus TI/Common/Virus Control.dll" \
  '.rsrc/0/XML/*' -y
```

`wrestool` from `icoutils` works equally well for the second step and preserves
the resource names.

The `.pkg` also works on Linux — its payloads are ordinary gzip'd cpio:

```bash
sudo apt install p7zip-full cpio
7z x -o ~/virus-pkg "Virus TI Software Suite 5.1.7.00.pkg"
7z e -so ~/virus-pkg/Core_components.pkg/Payload > /tmp/payload.cpio
cd ~/virus-xml && cpio -idmu --no-absolute-filenames -F /tmp/payload.cpio '*remotedevice*.xml'
```

## Reading it

Each `<Parameter>` carries the bank and index that form a live-edit message:

```text
F0 00 20 33 01 00 <bank> <part> <index> <value> F7
```

Banks appear in the XML in **decimal** — `115` is `0x73`. Bank *letters* are
inconsistent between Access's own documents, so cite the hex byte.

A parameter entry names its value list, and the list gives every label:

```xml
<Parameter name="Mode" bank="115" index="122" min="0" max="3" valuelist="Val Playmodes"/>
```

## The one format trap

In a `type="mapped"` value list, **`value` is the wire value and `index` is the
display slot** — they are not interchangeable, and reading them the wrong way
round silently corrupts every enum. The label text is the element's own text
content, not an attribute.

## Verified on

Every route above was executed, and all seven XMLs are **byte-identical**
between the Windows `.msi` and the macOS `.pkg` — the choice of route is
convenience only.

| Route                                       | Verified on                    |
| ------------------------------------------- | ------------------------------ |
| `pkgutil --expand-full`                     | macOS 26.5.2, arm64            |
| `xar` + `gunzip` + `cpio`                   | macOS 26.5.2, arm64            |
| `msiextract` + `7z`, x86 and x64 MSIs       | Ubuntu 26.04, x86-64           |
| `msiextract` + `wrestool`                   | Ubuntu 26.04, x86-64           |
| `.pkg` via `7z` + `cpio`                    | Ubuntu 26.04, x86-64           |

`remotedevice.xml` from the 5.1.7.00 suite is 605,496 bytes,
`md5 f2965d34baf52cddde81a6c70da52a1f`. macOS spells the check `md5 -q file`;
`shasum -a 256` works on both platforms.
