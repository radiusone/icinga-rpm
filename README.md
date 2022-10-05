# icinga-rpm

Spec files to build Icinga RPMs

## Instructions

* Clone this repository into `~/rpmbuild`
* Use `dnf` to install build dependencies
* Build the RPMs
* Stage into your repository server

Example:
```
git clone https://github.com/radiusone/icinga-rpm.git ~/rpmbuild
dnf builddep ~/rpmbuild/SPECS/*.spec
rpmbuild -bb --undefine _disable_source_fetch ~/rpmbuild/SPECS/*.spec
scp ~/rpmbuild/RPMS/*.rpm repo_server:/my/repo/dir/
```

(Sources are not fetched by default: either use the `--undefine` option as above,
edit your `/etc/rpmrc` file to undefine it, or pre-fetch the sources.)
