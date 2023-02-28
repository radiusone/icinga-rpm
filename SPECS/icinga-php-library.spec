# Icinga PHP Library for Icinga Web 2 | (c) 2021 Icinga GmbH | GPLv2+

%global revision 1
%global module_name icinga-php-library

Name:           %{module_name}
Version:        0.10.1
Release:        %{revision}%{?dist}
Summary:        Icinga PHP Library for Icinga Web 2
Group:          Applications/System
License:        MIT
URL:            https://icinga.com
Source0:        https://github.com/Icinga/%{module_name}/archive/v%{version}.tar.gz
BuildArch:      noarch

%global basedir %{_datadir}/icinga-php/ipl

Requires:       icinga-php-common
Requires:       icinga-php-thirdparty

# php extension requirements
Requires:                   php-intl
%{?rhel:Requires:           php-pdo}
%{?suse_version:Requires:   php-gettext php-json php-openssl}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
Requires:                   php-json
%endif

%description
This project bundles all Icinga PHP libraries into one
piece and can be integrated as library into Icinga Web 2.

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
* Wed Jul 06 2022 Johannes Meyer <johannes.meyer@icinga.com> - 0.9.1-1
- Release 0.9.1

* Thu Jun 30 2022 Henrik Triem <henrik.triem@icinga.com> - 0.9.0-1
- Release 0.9.0

* Tue Apr 26 2022 Johannes Meyer <johannes.meyer@icinga.com> - 0.8.1-1
- Release 0.8.1

* Wed Mar 23 2022 Johannes Meyer <johannes.meyer@icinga.com> - 0.8.0-1
- Release 0.8.0

* Wed Nov 10 2021 Johannes Meyer <johannes.meyer@icinga.com> - 0.7.0-1
- Release 0.7.0

* Tue Jul 27 2021 Johannes Meyer <johannes.meyer@icinga.com> - 0.6.1-1
- Release 0.6.1

* Thu Jul 08 2021 Henrik Triem <henrik.triem@icinga.com> - 0.6.0-1
- Release 0.6.0
