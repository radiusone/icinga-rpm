# Icinga DB Web for Icinga Web 2 | (c) 2021 Icinga GmbH | GPLv2+

%global revision 1
%global module_name icingadb

Name:           icingadb-web
Version:        1.0.0
Release:        %{revision}%{?dist}
Summary:        Icinga DB Web for Icinga Web 2
Group:          Applications/System
License:        GPLv2+
URL:            https://icinga.com
Source0:        https://github.com/Icinga/icingadb-web/archive/v%{version}.tar.gz
BuildArch:      noarch

%global basedir %{_datadir}/icingaweb2/modules/icingadb
%global docdir %{_datadir}/doc/icingadb-web

Requires:       icingaweb2 >= 2.9
Requires:       icinga-php-library
Requires:       icinga-php-thirdparty

%description
Icinga DB Web offers a modern and streamlined design to provide a clear
and concise overview of your monitoring environment.

%prep
%setup

%install
mkdir -vp %{buildroot}%{basedir}
mkdir -vp %{buildroot}%{docdir}

cp -vr application %{buildroot}%{basedir}
cp -vr library %{buildroot}%{basedir}
cp -vr public %{buildroot}%{basedir}
cp -vr configuration.php %{buildroot}%{basedir}
cp -vr module.info %{buildroot}%{basedir}
cp -vr run.php %{buildroot}%{basedir}

cp -vr doc %{buildroot}%{docdir}

%clean
rm -rf %{buildroot}

%preun
set -e

# Only for removal
if [ $1 == 0 ]; then
    echo "Disabling icingaweb2 module '%{module_name}'"
    rm -f /etc/icingaweb2/enabledModules/%{module_name}
fi

exit 0

%files
%doc README.md
%license LICENSE
%defattr(-,root,root)
%{basedir}
%{docdir}

%changelog
* Fri Oct 29 2021 Henrik Triem <henrik.triem@icinga.com> - 1.0.0-2
- Release Version 1.0.0

* Tue Aug 17 2021 Henrik Triem <henrik.triem@icinga.com> - 1.0.0-1
- Release Version 1.0.0
