# Icinga Web 2 | (c) 2013-2017 Icinga Development Team | GPLv2+

%define revision 1

Name:           icingaweb2
Version:        2.11.1
Release:        %{revision}%{?dist}
Summary:        Icinga Web 2
Group:          Applications/System
License:        GPLv2+ and MIT and BSD
URL:            https://icinga.com
Source0:        https://github.com/Icinga/%{name}/archive/v%{version}.tar.gz
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
Packager:       Icinga GmbH <info@icinga.com>

%if 0%{?fedora} || 0%{?rhel} || 0%{?amzn}
%if 0%{?rhel} == 7
%define php_scl         rh-php73
%endif

%if 0%{?el5}%{?el6}%{?amzn}
%define use_selinux 0
%else
%define use_selinux 1
%endif

%if 0%{?php_scl:1}
%define php_scl_prefix  %{php_scl}-
%define php_runtime     %{php_scl_prefix}php-fpm
%define php_bin         /opt/rh/%{php_scl}/root/usr/bin/php
%define php_fpm         1
%else
%define php_runtime     %{php}
%endif

%define php             %{?php_scl_prefix}php
%define php_cli         %{php}-cli
%define php_common      %{php}-common
%define wwwconfigdir    %{_sysconfdir}/httpd/conf.d
%define wwwuser         apache

# extra requirements on RHEL
Requires:               %{php}-mysqlnd
Requires:               %{php}-pgsql
Requires:               %{php}-ldap
%endif

# minimum required PHP version
%define php_version 7.2

# unsupported PHP version
%define php_unsupported_version 8.2

%if 0%{?suse_version}
%define wwwconfigdir    %{_sysconfdir}/apache2/conf.d
%define wwwuser         wwwrun
%define php             php
%define php_runtime     mod_php_any
%define php_common      %{php}
%define php_cli         %{php}
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
Requires:                       icinga-php-library >= 0.9.0-1
Requires:                       icinga-php-thirdparty >= 0.11.0-1
Requires:                       %{name}-vendor-dompdf = %{version}-%{release}
Requires:                       %{name}-vendor-HTMLPurifier = 1:%{version}-%{release}
Requires:                       %{name}-vendor-JShrink = %{version}-%{release}
Requires:                       %{name}-vendor-lessphp = %{version}-%{release}
Requires:                       %{name}-vendor-Parsedown = %{version}-%{release}

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
Requires:                   %{php}-gd %{php}-intl %{php}-mbstring
%if 0%{?sle_version} >= 150200
Requires:                   %{php}-dom %{php}-curl %{php}-fileinfo
%endif
%{?rhel:Requires:           %{php}-pdo %{php}-xml}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
Requires:                   %{php}-json
%endif rhel >= 8 || fedora >= 30
Requires:                   %{name}-vendor-zf1 = %{version}-%{release}
%{?amzn:Requires:           %{php}-pecl-imagick}
%{?fedora:Requires:         php-pecl-imagick}
%{?suse_version:Requires:   %{php}-gettext %{php}-json %{php}-openssl %{php}-posix}

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


%package vendor-dompdf
Summary:    Icinga Web 2 vendor library dompdf
Group:      Development/Libraries
License:    LGPLv2.1
Requires:   %{php_common} >= %{php_version}
Requires:   %{name}-common = %{version}-%{release}

%description vendor-dompdf
Icinga Web 2 vendor library dompdf


%package vendor-HTMLPurifier
Epoch:      1
Summary:    Icinga Web 2 vendor library HTMLPurifier
Group:      Development/Libraries
License:    LGPLv2.1
Requires:   %{php_common} >= %{php_version}
Requires:   %{name}-common = %{version}-%{release}

%description vendor-HTMLPurifier
Icinga Web 2 vendor library HTMLPurifier


%package vendor-JShrink
Summary:    Icinga Web 2 vendor library JShrink
Group:      Development/Libraries
License:    BSD
Requires:   %{php_common} >= %{php_version}
Requires:   %{name}-common = %{version}-%{release}

%description vendor-JShrink
Icinga Web 2 vendor library JShrink


%package vendor-lessphp
Summary:    Icinga Web 2 vendor library lessphp
Group:      Development/Libraries
License:    MIT
Requires:   %{php_common} >= %{php_version}
Requires:   %{name}-common = %{version}-%{release}

%description vendor-lessphp
Icinga Web 2 vendor library lessphp


%package vendor-Parsedown
Summary:    Icinga Web 2 vendor library Parsedown
Group:      Development/Libraries
License:    MIT
Requires:   %{php_common} >= %{php_version}
Requires:   %{name}-common = %{version}-%{release}

%description vendor-Parsedown
Icinga Web 2 vendor library Parsedown


%package vendor-zf1
Summary:    Icinga Web 2's fork of Zend Framework 1
Group:      Development/Libraries
License:    BSD
Requires:   %{php_common} >= %{php_version}
Obsoletes:  %{name}-vendor-Zend < 1.12.20
Requires:   %{name}-common = %{version}-%{release}

%description vendor-zf1
Icinga Web 2's fork of Zend Framework 1


%prep
%setup -q
%if 0%{?use_selinux}
mkdir selinux
cp -p packages/selinux/icingaweb2.{fc,if,te} selinux
%endif

%build
%if 0%{?use_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv icingaweb2.pp icingaweb2.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/{%{basedir}/{modules,library/vendor,public},%{bindir},%{configdir}/modules,%{storagedir},%{logdir},%{phpdir},%{wwwconfigdir},%{_sysconfdir}/bash_completion.d,%{docsdir}}
cp -prv application doc %{buildroot}/%{basedir}
cp -pv etc/bash_completion.d/icingacli %{buildroot}/%{_sysconfdir}/bash_completion.d/icingacli
cp -prv modules/{monitoring,setup,doc,translation,migrate} %{buildroot}/%{basedir}/modules
cp -prv library/Icinga %{buildroot}/%{phpdir}
cp -prv library/vendor/{dompdf,HTMLPurifier*,JShrink,lessphp,Parsedown,Zend} %{buildroot}/%{basedir}/library/vendor
cp -prv public/{css,font,img,js,error_norewrite.html,error_unavailable.html} %{buildroot}/%{basedir}/public
%if 0%{?php_fpm:1}
cp -pv packages/files/apache/icingaweb2.fpm.conf %{buildroot}/%{wwwconfigdir}/icingaweb2.conf
%else
cp -pv packages/files/apache/icingaweb2.conf %{buildroot}/%{wwwconfigdir}/icingaweb2.conf
%endif
cp -pv packages/files/bin/icingacli %{buildroot}/%{bindir}
%if 0%{?php_bin:1}
sed -i '1 s~#!.*~#!%{php_bin}~' %{buildroot}/%{bindir}/icingacli
%endif
cp -pv packages/files/public/index.php %{buildroot}/%{basedir}/public
cp -prv etc/schema %{buildroot}/%{docsdir}
cp -prv packages/files/config/modules/{setup,translation} %{buildroot}/%{configdir}/modules
%if 0%{?use_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 icingaweb2.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/icingaweb2.pp
done
cd -
# TODO: Fix build problems on Icinga, see https://github.com/Icinga/puppet-icinga_build/issues/11
#/usr/sbin/hardlink -cv %{buildroot}%{_datadir}/selinux
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
%dir %{basedir}/library/vendor
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
%doc selinux/*
%{_datadir}/selinux/*/icingaweb2.pp
%endif


%files vendor-dompdf
%defattr(-,root,root)
%{basedir}/library/vendor/dompdf


%files vendor-HTMLPurifier
%defattr(-,root,root)
%{basedir}/library/vendor/HTMLPurifier
%{basedir}/library/vendor/HTMLPurifier.autoload.php
%{basedir}/library/vendor/HTMLPurifier.php


%files vendor-JShrink
%defattr(-,root,root)
%{basedir}/library/vendor/JShrink


%files vendor-lessphp
%defattr(-,root,root)
%{basedir}/library/vendor/lessphp


%files vendor-Parsedown
%defattr(-,root,root)
%{basedir}/library/vendor/Parsedown


%files vendor-zf1
%defattr(-,root,root)
%{basedir}/library/vendor/Zend

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
