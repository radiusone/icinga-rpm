# Icinga Web 2 | (c) 2013-2017 Icinga Development Team | GPLv2+

%define revision 0

Name:           icingaweb2
Version:        2.12.2
Release:        %{revision}%{?dist}
Summary:        Icinga Web 2
Group:          Applications/System
License:        GPLv2+ and MIT and BSD
URL:            https://icinga.com
Source0:        https://github.com/Icinga/%{name}/archive/v%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
Packager:       Icinga GmbH <info@icinga.com>

Source1:        icingaweb2.fc
Source2:        icingaweb2.te
Source3:        icingaweb2.sh
Source4:        icingaweb2.if
Source5:        icingaweb2.conf
Source6:        icingaweb2.fpm.conf
Source7:        icingaweb2.index.php
Source8:        icingacli
Source9:        icingaweb2.doc.config.ini
Source10:       icingaweb2.setup.config.ini
Source11:       icingaweb2.translation.config.ini

%if 0%{?fedora} || 0%{?rhel} || 0%{?amzn}

%if 0%{?el5}%{?el6}%{?amzn}
%define use_selinux 0
%else
%define use_selinux 1
%endif

%define php_runtime     php
%define php_cli         php-cli
%define php_common      php-common
%define wwwconfigdir    %{_sysconfdir}/httpd/conf.d
%define wwwuser         apache

# extra requirements on RHEL
Requires:               php-mysqlnd
Requires:               php-pgsql
Requires:               php-ldap
%endif

# minimum required PHP version
%define php_version 7.2

# unsupported PHP version
%define php_unsupported_version 8.4

%if 0%{?suse_version}
%define wwwconfigdir    %{_sysconfdir}/apache2/conf.d
%define wwwuser         wwwrun
%define php_runtime     mod_php_any
%define php_common      php
%define php_cli         php
%endif

%{?amzn:Requires(pre):          shadow-utils}
%{?fedora:Requires(pre):        shadow-utils}
%{?rhel:Requires(pre):          shadow-utils}
%{?suse_version:Requires(pre):  pwdutils}

Requires:                       %{php_runtime} >= %{php_version}
Requires:                       %{php_common} >= %{php_version}
Conflicts:                      %{php_runtime} >= %{php_unsupported_version}
%if 0%{?suse_version}
Requires:                       apache2
%endif

Requires:                       icinga-l10n >= 1.1.0-1
Requires:                       icingacli = %{version}-%{release}
Requires:                       %{name}-common = %{version}-%{release}
Requires:                       php-Icinga = %{version}-%{release}
Requires:                       icinga-php-library >= 0.13.0-1
Requires:                       icinga-php-thirdparty >= 0.12.0-1

%define basedir         %{_datadir}/%{name}
%define bindir          %{_bindir}
%define storagedir      %{_sharedstatedir}/%{name}
%define configdir       %{_sysconfdir}/%{name}
%define logdir          %{_localstatedir}/log/%{name}
%define phpdir          %{_datadir}/php
%define icingawebgroup  icingaweb2
%define docsdir         %{_datadir}/doc/%{name}


%description
Icinga Web 2


%package common
Summary:                        Common files for Icinga Web 2 and the Icinga CLI
Group:                          Applications/System
%{?amzn:Requires(pre):          shadow-utils}
%{?fedora:Requires(pre):        shadow-utils}
%{?rhel:Requires(pre):          shadow-utils}
%{?suse_version:Requires(pre):  pwdutils}
%if 0%{?suse_version} > 1320
Requires(pre):                  system-user-wwwrun
%endif

%description common
Common files for Icinga Web 2 and the Icinga CLI


%package -n php-Icinga
Summary:                    Icinga Web 2 PHP library
Group:                      Development/Libraries
Requires:                   %{php_common} >= %{php_version}
Requires:                   php-gd php-intl php-mbstring
%if 0%{?sle_version} >= 150200
Requires:                   php-dom php-curl php-fileinfo
%endif
%{?rhel:Requires:           php-pdo php-xml}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
Requires:                   php-json
%endif
%{?amzn:Requires:           php-pecl-imagick}
%{?fedora:Requires:         php-pecl-imagick}
%{?suse_version:Requires:   php-gettext php-json php-openssl php-posix}

%description -n php-Icinga
Icinga Web 2 PHP library


%package -n icingacli
Summary:                    Icinga CLI
Group:                      Applications/System
Requires:                   icinga-l10n >= 1.1.0-1
Requires:                   %{name}-common = %{version}-%{release}
Requires:                   php-Icinga = %{version}-%{release}
Requires:                   icinga-php-library >= 0.9.0-1
Requires:                   icinga-php-thirdparty >= 0.11.0-1
Requires:                   bash-completion
Requires:                   %{php_cli} >= %{php_version}


%description -n icingacli
Icinga CLI


%if 0%{?use_selinux}
%define selinux_variants mls targeted

%package selinux
Summary:        SELinux policy for Icinga Web 2
BuildRequires:  checkpolicy, selinux-policy-devel, hardlink
Requires:           %{name} = %{version}-%{release}
Requires(post):     policycoreutils
Requires(postun):   policycoreutils

%description selinux
SELinux policy for Icinga Web 2
%endif


%prep
%setup -q

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{basedir}/{modules,library,public},%{bindir},%{configdir}/modules,%{storagedir},%{logdir},%{phpdir},%{wwwconfigdir},%{_sysconfdir}/bash_completion.d,%{docsdir}}
cp -prv application doc %{buildroot}/%{basedir}
cp -pv etc/bash_completion.d/icingacli %{buildroot}/%{_sysconfdir}/bash_completion.d/icingacli
cp -prv modules/{monitoring,setup,doc,translation,migrate} %{buildroot}/%{basedir}/modules
cp -prv library/Icinga %{buildroot}/%{phpdir}
cp -prv public/{css,font,img,js,error_norewrite.html,error_unavailable.html} %{buildroot}/%{basedir}/public
%if 0%{?php_fpm:1}
cp -pv %{SOURCE6} %{buildroot}/%{wwwconfigdir}/icingaweb2.conf
%else
cp -pv %{SOURCE5} %{buildroot}/%{wwwconfigdir}/icingaweb2.conf
%endif
cp -pv %{SOURCE8} %{buildroot}/%{bindir}
%if 0%{?php_bin:1}
sed -i '1 s~#!.*~#!%{php_bin}~' %{buildroot}/%{bindir}/icingacli
%endif
cp -pv %{SOURCE7} %{buildroot}/%{basedir}/public/index.php
cp -prv schema %{buildroot}/%{docsdir}
mkdir -p %{buildroot}/%{configdir}/modules/setup
cp -pv %{SOURCE10} %{buildroot}/%{configdir}/modules/setup/config.ini
mkdir -p %{buildroot}/%{configdir}/modules/translation
cp -pv %{SOURCE11} %{buildroot}/%{configdir}/modules/translation/config.ini
%if 0%{?use_selinux}
mkdir -p %{buildroot}%{_docdir}
cp %{SOURCE1} %{buildroot}%{_docdir}
cp %{SOURCE2} %{buildroot}%{_docdir}
cp %{SOURCE3} %{buildroot}%{_docdir}
cp %{SOURCE4} %{buildroot}%{_docdir}
cd %{buildroot}%{_docdir}
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 icingaweb2.pp %{buildroot}%{_datadir}/selinux/${selinuxvariant}/icingaweb2.pp
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -
%endif

%pre
getent group icingacmd >/dev/null || groupadd -r icingacmd
%if 0%{?suse_version} && 0%{?suse_version} < 01200
usermod -A icingacmd,%{icingawebgroup} %{wwwuser}
%else
usermod -a -G icingacmd,%{icingawebgroup} %{wwwuser}
%endif
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{basedir}/application/controllers
%{basedir}/application/fonts
%{basedir}/application/forms
%{basedir}/application/layouts
%{basedir}/application/views
%{basedir}/application/VERSION
%{basedir}/doc
%{basedir}/modules
%{basedir}/public
%if 0%{?suse_version}
# for lint on OBS
%dir %{dirname:%{wwwconfigdir}}
%dir %{wwwconfigdir}
%endif
%config(noreplace) %{wwwconfigdir}/icingaweb2.conf
%attr(2775,root,%{icingawebgroup}) %dir %{logdir}
%attr(2770,root,%{icingawebgroup}) %config(noreplace) %dir %{configdir}/modules/setup
%attr(0660,root,%{icingawebgroup}) %config(noreplace) %{configdir}/modules/setup/config.ini
%attr(2770,root,%{icingawebgroup}) %config(noreplace) %dir %{configdir}/modules/translation
%attr(0660,root,%{icingawebgroup}) %config(noreplace) %{configdir}/modules/translation/config.ini
%{docsdir}
%docdir %{docsdir}


%pre common
getent group %{icingawebgroup} >/dev/null || groupadd -r %{icingawebgroup}
exit 0

%files common
%defattr(-,root,root)
%dir %{basedir}
%dir %{basedir}/application
%dir %{basedir}/library
%dir %{basedir}/modules
%attr(2770,root,%{icingawebgroup}) %dir %{storagedir}
%attr(2770,root,%{icingawebgroup}) %config(noreplace) %dir %{configdir}
%attr(2770,root,%{icingawebgroup}) %config(noreplace) %dir %{configdir}/modules


%files -n php-Icinga
%defattr(-,root,root)
%if 0%{?suse_version}
# for lint on OBS
%dir %{phpdir}
%endif
%{phpdir}/Icinga


%files -n icingacli
%defattr(-,root,root)
%{basedir}/application/clicommands
%{_sysconfdir}/bash_completion.d/icingacli
%attr(0755,root,root) %{bindir}/icingacli


%if 0%{?use_selinux}
%post selinux
for selinuxvariant in %{selinux_variants}
do
  %{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/icingaweb2.pp &> /dev/null || :
done
%{_sbindir}/restorecon -R %{basedir} &> /dev/null || :
%{_sbindir}/restorecon -R %{configdir} &> /dev/null || :
%{_sbindir}/restorecon -R %{logdir} &> /dev/null || :
%{_sbindir}/restorecon -R %{storagedir} &> /dev/null || :


%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
     %{_sbindir}/semodule -s ${selinuxvariant} -r icingaweb2 &> /dev/null || :
  done
  [ -d %{basedir} ] && %{_sbindir}/restorecon -R %{basedir} &> /dev/null || :
  [ -d %{configdir} ] && %{_sbindir}/restorecon -R %{configdir} &> /dev/null || :
  [ -d %{logdir} ] && %{_sbindir}/restorecon -R %{logdir} &> /dev/null || :
  [ -d %{storagedir} ] && %{_sbindir}/restorecon -R %{storagedir} &> /dev/null || :
fi

%files selinux
%defattr(-,root,root,0755)
%doc %{_docdir}/*
%{_datadir}/selinux/*/icingaweb2.pp
%endif


%changelog
* Wed Jul 06 2022 Johannes Meyer <johannes.meyer@icinga.com> 2.11.1-1
- Update to 2.11.1

* Thu Jun 30 2022 Eric Lippmann <eric.lippmann@icinga.com> 2.11.0-1
- Update to 2.11.0

* Wed Apr 06 2022 Johannes Meyer <johannes.meyer@icinga.com> 2.10.1-1
- Update to 2.10.1

* Wed Mar 23 2022 Johannes Meyer <johannes.meyer@icinga.com> 2.10.0-1
- Update to 2.10.0

* Tue Mar 08 2022 Johannes Meyer <johannes.meyer@icinga.com> 2.9.6-1
- Update to 2.9.6

* Thu Nov 18 2021 Henrik Triem <henrik.triem@icinga.com> 2.9.5-1
- Update to 2.9.5

* Wed Nov 10 2021 Johannes Meyer <johannes.meyer@icinga.com> 2.9.4-1
- Update to 2.9.4

* Tue Aug 10 2021 Johannes Meyer <johannes.meyer@icinga.com> 2.9.3-1
- Update to 2.9.3

* Wed Jul 28 2021 Johannes Meyer <johannes.meyer@icinga.com> 2.9.2-1
- Update to 2.9.2

* Tue Jul 27 2021 Johannes Meyer <johannes.meyer@icinga.com> 2.9.1-1
- Update to 2.9.1

* Thu Jul 8 2021 Johannes Meyer <johannes.meyer@icinga.com> 2.9.0-1
- Update to 2.9.0

* Tue Aug 18 2020 Johannes Meyer <johannes.meyer@icinga.com> 2.8.2-1
- Update to 2.8.2

* Mon Jun 29 2020 Johannes Meyer <johannes.meyer@icinga.com> 2.8.1-1
- Update to 2.8.1

* Mon Jun 8 2020 Johannes Meyer <johannes.meyer@icinga.com> 2.8.0-1
- Update to 2.8.0
- Add new requirement for package icinga-l10n
- [EPEL 7] We now require PHP 7.3 instead of PHP 7.1
- Please check uprading docs at /usr/share/icingaweb2/doc/80-Upgrading.md

* Fri Oct 18 2019 Johannes Meyer <johannes.meyer@icinga.com> 2.7.3-1
- Update to 2.7.3

* Wed Oct 16 2019 Johannes Meyer <johannes.meyer@icinga.com> 2.7.2-1
- Update to 2.7.2

* Wed Aug 14 2019 Johannes Meyer <johannes.meyer@icinga.com> 2.7.1-1
- Update to 2.7.1

* Tue Jul 30 2019 Johannes Meyer <johannes.meyer@icinga.com> 2.7.0-1
- Update to 2.7.0

* Wed Apr 24 2019 Johannes Meyer <johannes.meyer@icinga.com> 2.6.3-1
- Update to 2.6.3

* Wed Nov 21 2018 Eric Lippmann <eric.lippmann@icinga.com> 2.6.2-1
- Update to 2.6.2

* Thu Aug 02 2018 Eric Lippmann <eric.lippmann@icinga.com> 2.6.1-1
- Update to 2.6.1

* Thu Jul 19 2018 Blerim Sheqa <blerim.sheqa@icinga.com> 2.6.0-1
- Update to 2.6.0

* Fri Apr 27 2018 Eric Lippmann <eric.lippmann@icinga.com> 2.5.3-1
- Update to 2.5.3

* Thu Apr 26 2018 Eric Lippmann <eric.lippmann@icinga.com> 2.5.2-1
- Update to 2.5.2

* Mon Jan 22 2018 Markus Frosch <markus.frosch@icinga.com> 2.5.1-1
- Update to 2.5.1
- Remove FPM patches

* Wed Nov 29 2017 Eric Lippmann <eric.lippmann@icinga.com> 2.5.0-2
- FPM: Add patch to support both Apache >= 2.4 and Apache < 2.4

* Tue Nov 28 2017 Eric Lippmann <eric.lippmann@icinga.com> 2.5.0-1
- Install error_unavailable.html
- Add patch to fix Apache FPM config

* Mon Nov 27 2017 Markus Frosch <markus.frosch@icinga.com> 2.5.0-1
- Update to 2.5.0
- All packages now require PHP >= 5.6
- [EPEL 6 + 7] We now require PHP 7 from SCL packages, php-fpm as runtime engine
- [SUSE / openSUSE] Requirements will force the installation of php7
- Please check upgrading docs at /usr/share/icingaweb2/doc/80-Upgrading.md

* Thu Sep 28 2017 Markus Frosch <markus.frosch@icinga.com> 2.4.2-1
- Update to 2.4.2
