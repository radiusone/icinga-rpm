# Icinga PHP Common for Icinga Web 2 | (c) 2021 Icinga GmbH | GPLv2+

%global revision 1

Name:           icinga-php-common
Version:        1.0.0
Release:        %{revision}%{?dist}
Summary:        Icinga PHP Common for Icinga Web 2
Group:          Applications/System
License:        Public Domain
URL:            https://icinga.com
BuildArch:      noarch

%global basedir %{_datadir}/icinga-php

%description
This package manages the directory /usr/share/icinga-php.

%install
mkdir -vp %{buildroot}%{basedir}

%files
%defattr(-,root,root)
%{basedir}

%changelog
* Thu Jul 08 2021 Henrik Triem <henrik.triem@icinga.com> - 1.0.0-1
- Release 1.0.0
