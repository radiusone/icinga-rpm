# Icinga PHP Thirdparty for Icinga Web 2 | (c) 2021 Icinga GmbH | GPLv2+

%global revision 1
%global module_name icinga-php-thirdparty

Name:           %{module_name}
Version:        0.11.0
Release:        %{revision}%{?dist}
Summary:        Icinga PHP Thirdparty for Icinga Web 2
Group:          Applications/System
License:        MIT
URL:            https://icinga.com
Source0:        https://github.com/Icinga/%{module_name}/archive/v%{version}.tar.gz
BuildArch:      noarch

%global basedir %{_datadir}/icinga-php/vendor

Requires:       icinga-php-common

# php extension requirements
Requires:                   php-soap
Requires:                   php-sockets
Requires:                   php-curl
%{?suse_version:Requires:   php-json}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
Requires:                   php-json
%endif

%description
This package bundles all 3rd party PHP libraries
used by Icinga Web products into one piece,
which can be integrated as library into Icinga Web 2.

%prep
%setup -q

%install
mkdir -vp %{buildroot}%{basedir}

cp -vr asset %{buildroot}%{basedir}
cp -vr vendor %{buildroot}%{basedir}
cp -vr composer.* %{buildroot}%{basedir}
cp -vr VERSION %{buildroot}%{basedir}

%clean
rm -rf %{buildroot}

%files
%doc README.md
%license LICENSE
%defattr(-,root,root)
%{basedir}

%changelog
* Thu Jun 30 2022 Henrik Triem <henrik.triem@icinga.com> - 0.11.0-1
- Release 0.11.0

* Tue Jul 27 2021 Johannes Meyer <johannes.meyer@icinga.com> - 0.10.0-2
- Added missing php extension requirements

* Thu Jul 08 2021 Henrik Triem <henrik.triem@icinga.com> - 0.10.0-1
- Release 0.10.0
