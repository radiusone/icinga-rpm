%define revision 0

%global provider        github
%global provider_tld    com
%global project         Icinga
%global repo            icingadb
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:       icingadb
Version:    1.3.0
Release:    %{revision}%{?dist}
Summary:    Icinga DB
Group:      System Environment/Daemons
%if "%{_vendor}" == "suse"
License:    GPL-2.0-or-later
%else
License:    GPLv2+
%endif
URL:        https://%{provider_prefix}
Source0:    https://%{import_path}/archive/v%{version}.tar.gz
Source1:    icingadb.service

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: gcc
BuildRequires: git
%if "%{_vendor}" == "suse"
BuildRequires: go >= 1.24.1
%else
BuildRequires: golang >= 1.24.1
%endif

%{?systemd_requires}
BuildRequires: systemd

%define debug_package %nil

%if "%{_vendor}" == "suse"
PreReq:         permissions
Provides:       user(icingadb)
Provides:       group(icingadb)
Requires(pre):  shadow
Requires(post): shadow
%else
Requires(pre):  shadow-utils
%endif

%define configdir %{_sysconfdir}/%{name}
%define service %{name}.service

%description
Icinga DB

%prep
%setup -q

go build -buildvcs=false -trimpath ./cmd/icingadb

%install
install -d -m 0755 %{buildroot}%{_sbindir}
install -d -m 0755 %{buildroot}%{configdir}
install -d -m 0755 %{buildroot}%{_unitdir}

install -m 0755 icingadb %{buildroot}%{_sbindir}/
install -m 0644 config.example.yml %{buildroot}%{configdir}/config.yml
install -m 0644 %{S:1} %{buildroot}%{_unitdir}/

install -d -m 0755 %{buildroot}%{_datadir}/%{name}
(umask 0022 && cp -rv schema %{buildroot}%{_datadir}/%{name}/)

%if "%{_vendor}" == "suse"
ln -sf /usr/sbin/service %{buildroot}%{_sbindir}/rc%{name}
%endif

%pre
getent group icingadb >/dev/null || groupadd -r icingadb
getent passwd icingadb >/dev/null || useradd -r -g icingadb -d /etc/icingadb -s /sbin/nologin -c 'Icinga DB' icingadb

%if "%{_vendor}" == "suse"
%service_add_pre %{service}
%endif

%post
%if "%{_vendor}" == "suse"
%service_add_post %{service}
%else
%systemd_post %{service}
%endif

%preun
%if "%{_vendor}" == "suse"
%service_del_preun %{service}
%else
%systemd_preun %{service}
%endif

%postun
%if "%{_vendor}" == "suse"
%service_del_postun %{service}
%else
%systemd_postun %{service}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc LICENSE AUTHORS README.md CHANGELOG.md
%{_sbindir}/icingadb
%{_unitdir}/%{service}

%if "%{_vendor}" == "suse"
%{_sbindir}/rc%{name}
%endif

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/schema

%defattr(0644,icingadb,icingadb,0755)

%dir %{configdir}
%config(noreplace) %{configdir}/config.yml

%changelog
* Fri Oct 29 2021 Henrik Triem <henrik.triem@icinga.com> 1.0.0-2
* Fri Dec 13 2019 Henrik Triem <henrik.triem@icinga.com> 0.0.0-1
* Mon Sep 24 2018 Markus Frosch <markus.frosch@icinga.com> 0.0.0-0
- Initial package
