# Icinga 2 | (c) 2012 Icinga GmbH | GPLv2+

%define revision 0

# make sure that _rundir is working on older systems
%if ! %{defined _rundir}
%define _rundir %{_localstatedir}/run
%endif
%if ! %{defined _fillupdir}
  %define _fillupdir %{_localstatedir}/adm/fillup-templates
%endif

%define _libexecdir %{_prefix}/lib/
%define plugindir %{_libdir}/nagios/plugins

%if "%{_vendor}" == "redhat"
%define apachename httpd
%define apacheconfdir %{_sysconfdir}/httpd/conf.d
%define apacheuser apache
%define apachegroup apache

%if 0%{?amzn}
%define use_systemd 0
%define use_selinux 0
%if %(uname -m) != "x86_64"
%define march_flag -march=i686
%endif
%else
# fedora and el>=7
%define use_systemd 1
%define use_selinux 1
%if 0%{?fedora} >= 24
# for installing limits.conf on systemd >= 228
%define configure_systemd_limits 1
%else
%define configure_systemd_limits 0
%endif
%endif
%endif

%if "%{_vendor}" == "suse"
%define plugindir %{_libexecdir}/nagios/plugins
%define apachename apache2
%define apacheconfdir  %{_sysconfdir}/apache2/conf.d
%define apacheuser wwwrun
%define apachegroup www
%if 0%{?suse_version} >= 1310
%define use_systemd 1
%if 0%{?sle_version} >= 120200 || 0%{?suse_version} > 1320
# for installing limits.conf on systemd >= 228
%define configure_systemd_limits 1
%else
%define configure_systemd_limits 0
%endif
%else
%define use_systemd 0
%endif
%endif

%define icinga_user icinga
%define icinga_group icinga
%define icingacmd_group icingacmd

# enable unity builds by default for all architectures except arm32
%ifarch %{arm}
%bcond_with unity_build
%else
%bcond_without unity_build
%endif

%bcond_with systemd_and_init
%bcond_without compat
%bcond_without livestatus
%bcond_without notification
%bcond_without perfdata
%bcond_without tests
%bcond_without mysql
%bcond_without pgsql

%define logmsg logger -t %{name}/rpm

%define boost_min_version 1.66

Summary:        Network monitoring application
%if "%{_vendor}" == "suse"
License:        GPL-2.0-or-later
%else
License:        GPLv2+
%endif
Group:          System/Monitoring
Name:           icinga2
Version:        2.14.3
Release:        %{revision}%{?dist}
Url:            https://www.icinga.com/
Source:         https://github.com/Icinga/%{name}/archive/v%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       %{name}-bin = %{version}-%{release}
Requires:       %{name}-common = %{version}-%{release}

Conflicts:      %{name}-common < %{version}-%{release}

%description
Meta package for Icinga 2 Core, DB IDO and Web.

%package bin
Summary:        Icinga 2 binaries and libraries
Group:          System/Monitoring

Requires:       %{name}-bin = %{version}-%{release}

%if "%{_vendor}" == "suse"
Provides:       monitoring_daemon
Recommends:     monitoring-plugins
%if 0%{?suse_version} >= 1310
BuildRequires:  libyajl-devel
%endif
%endif
BuildRequires:  libedit-devel
BuildRequires:  ncurses-devel
%if "%{_vendor}" == "redhat" && (0%{?el7} || 0%{?rhel} == 7 || "%{?dist}" == ".el7")
  # Requires devtoolset-11 scl
  %define scl_name devtoolset-11
  %define scl_enable scl enable %{scl_name} --
BuildRequires:  %{scl_name}-binutils
BuildRequires:  %{scl_name}-gcc-c++
BuildRequires:  %{scl_name}-libstdc++-devel
%else
BuildRequires:  gcc-c++
BuildRequires:  libstdc++-devel
%endif
BuildRequires:  openssl-devel
BuildRequires:  bison
BuildRequires:  cmake
BuildRequires:  flex >= 2.5.35
BuildRequires:  make

%if "%{_vendor}" == "suse"
  %if 0%{?suse_version} >= 1315
    # SLES 12 and OpenSUSE 42 or later
    %define boost_devel_pkg %nil
    %if 0%{?suse_version} < 1320
      # before SLES 15 and OpenSUSE 15
      # Provided by packages.icinga.com
      %define boost_library icinga-boost
      %define boost_version 1.69
      %define boost_rpath %{_libdir}/%{boost_library}
      # Note: the -impl suffix comes from current packages on OBS
      %define boost_devel_suffix -impl
    %endif
BuildRequires:  libboost_context-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_coroutine-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_filesystem-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_iostreams-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_program_options-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_regex-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_system-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_thread-devel%{?boost_devel_suffix} >= %{boost_min_version}
BuildRequires:  libboost_test-devel%{?boost_devel_suffix} >= %{boost_min_version}
  %else
    # suse_version < 1315
    # old boost devel name
    %define boost_devel_pkg boost-devel
  %endif
%else 
  # vendor != suse - assuming redhat or compatible
  # default boost devel package
  %define boost_devel_pkg boost-devel

  %if (0%{?el7} || 0%{?rhel} == 7)
    # Provided by EPEL
    %define boost_library boost169
    %define boost_version 1.69
    %define boost_devel_pkg boost169-devel
  %endif
%endif

%if "%{?boost_devel_pkg}" != ""
BuildRequires: %{boost_devel_pkg} >= %{boost_min_version}
%endif

%if 0%{?use_systemd}
BuildRequires:  systemd-devel
Requires:       systemd
%endif

Obsoletes:       %{name}-libs <= 2.10.0
Conflicts:       %{name}-libs <= 2.10.0

%description bin
Icinga 2 is a general-purpose network monitoring application.
This subpackage provides the binaries for Icinga 2 Core.

%package common
Summary:        Common Icinga 2 configuration
Group:          System/Monitoring
%if (0%{?amzn} || 0%{?fedora} || 0%{?rhel})
Requires(pre):  shadow-utils
Requires(post): shadow-utils
%endif
BuildRequires:  logrotate
%if "%{_vendor}" == "suse"
PreReq:         permissions
Provides:       group(%{icinga_group})
Provides:       group(%{icingacmd_group})
Provides:       user(%{icinga_user})
Requires(pre):  shadow
Requires(post): shadow
# Coreutils is added because of autoyast problems reported
Requires(pre):  coreutils
Requires(post): coreutils
%if 0%{?suse_version} >= 1200
BuildRequires:  monitoring-plugins-common
Requires:       monitoring-plugins-common
%else
Recommends:     monitoring-plugins-common
%endif
Recommends:     logrotate
%endif

%description common
This subpackage provides common directories, and the UID and GUID definitions
among Icinga 2 related packages.


%package doc
Summary:        Documentation for Icinga 2
Group:          Documentation/Other

%description doc
This subpackage provides documentation for Icinga 2.


%if %{with mysql}
%package ido-mysql
Summary:        IDO MySQL database backend for Icinga 2
Group:          System/Monitoring
%if "%{_vendor}" == "suse"
  BuildRequires:  libmysqlclient-devel
  %if 0%{?suse_version} >= 1310
    BuildRequires:  mysql-devel
  %endif

%else
  %if 0%{?rhel} >= 8
BuildRequires:  mariadb-connector-c-devel
  %else
BuildRequires:  mysql-devel
  %endif
%endif

Requires:       %{name}-bin = %{version}-%{release}

%description ido-mysql
Icinga 2 IDO mysql database backend. Compatible with Icinga 1.x
IDOUtils schema >= 1.12
%endif


%if %{with pgsql}
%package ido-pgsql
Summary:        IDO PostgreSQL database backend for Icinga 2
Group:          System/Monitoring
%if "%{_vendor}" == "suse" && 0%{?suse_version} < 1210
BuildRequires:  postgresql-devel >= 8.4
%else
BuildRequires:  postgresql-devel
%endif
Requires:       %{name}-bin = %{version}-%{release}

%description ido-pgsql
Icinga 2 IDO PostgreSQL database backend. Compatible with Icinga 1.x
IDOUtils schema >= 1.12
%endif

%if 0%{?use_selinux}
%global selinux_variants mls targeted
%global selinux_modulename %{name}

%package selinux
Summary:        SELinux policy module supporting icinga2
Group:          System/Base
BuildRequires:  checkpolicy
BuildRequires:  hardlink
BuildRequires:  selinux-policy-devel
Requires:       %{name}-bin = %{version}-%{release}
Requires:       icinga-selinux-common
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
Requires(post):   policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
%else
Requires(post):   policycoreutils-python
Requires(postun): policycoreutils-python
%endif


%description selinux
SELinux policy module supporting icinga2.
%endif

%package -n vim-icinga2
Summary:        Vim syntax highlighting for icinga2
Group:          Productivity/Text/Editors
%if "%{_vendor}" == "suse"
BuildRequires:  vim
Requires:       vim
%else
Requires:       vim-filesystem
%endif

%description -n vim-icinga2
Provides Vim syntax highlighting for icinga2.


%package -n nano-icinga2
Summary:        Nano syntax highlighting for icinga2
Group:          Productivity/Text/Editors
Requires:       nano

%description -n nano-icinga2
Provides Nano syntax highlighting for icinga2.

%prep
%setup -q -n %{name}-%{version}
# use absolute shebang instead of env on SUSE distributions
%if "%{_vendor}" == "suse"
find . -type f -name '*.sh' -exec sed -i -e 's|\/usr\/bin\/env bash|\/bin\/bash|g' {} \;
%endif

# quick & dirty hack for SLES11 & Kernel < 2.9 w/o SO_REUSEPORT
%if "%{_vendor}" == "suse" && 0%{?suse_version} < 1210
find . -type f -name tcpsocket.cpp -exec sed -i -e 's|.*SO_REUSEPORT.*||g' {} \;
%endif

%build
# set basedir to allow cache to hit between different builds
# this will make all paths below BUILD/icinga2-x.x.x relative for cache
export CCACHE_BASEDIR="${CCACHE_BASEDIR:-$(pwd)}"

CMAKE_OPTS="-DCMAKE_INSTALL_PREFIX=/usr \
         -DCMAKE_INSTALL_SYSCONFDIR=/etc \
         -DCMAKE_INSTALL_LOCALSTATEDIR=/var \
         -DCMAKE_BUILD_TYPE=RelWithDebInfo \
         -DCMAKE_VERBOSE_MAKEFILE=ON \
         -DBoost_NO_BOOST_CMAKE=ON \
         -DICINGA2_PLUGINDIR=%{plugindir} \
         -DICINGA2_RUNDIR=%{_rundir} \
         -DICINGA2_SYSCONFIGFILE=/etc/sysconfig/icinga2 \
         -DICINGA2_USER=%{icinga_user} \
         -DICINGA2_GROUP=%{icinga_group} \
         -DICINGA2_COMMAND_GROUP=%{icingacmd_group}"
%if 0%{?fedora}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_STUDIO=true"
%endif

%if %{with unity_build}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_UNITY_BUILD=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_UNITY_BUILD=OFF"
%endif

# Disable LTO build, see https://github.com/Icinga/icinga2/issues/7149
# lto1: internal compiler error: in prune_unused_types_prune, at dwarf2out.c
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_LTO_BUILD=OFF"

%if %{with systemd_and_init}
CMAKE_OPTS="$CMAKE_OPTS -DINSTALL_SYSTEMD_SERVICE_AND_INITSCRIPT=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DINSTALL_SYSTEMD_SERVICE_AND_INITSCRIPT=OFF"
%endif
%if %{with compat}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_COMPAT=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_COMPAT=OFF"
%endif
%if %{with livestatus}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_LIVESTATUS=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_LIVESTATUS=OFF"
%endif
%if %{with notification}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_NOTIFICATION=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_NOTIFICATION=OFF"
%endif
%if %{with perfdata}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_PERFDATA=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_PERFDATA=OFF"
%endif
%if %{with tests}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_TESTS=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_TESTS=OFF"
%endif
%if %{with mysql}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_MYSQL=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_MYSQL=OFF"
%endif
%if %{with pgsql}
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_PGSQL=ON"
%else
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_WITH_PGSQL=OFF"
%endif

%if "%{?boost_rpath}" != ""
CMAKE_OPTS="$CMAKE_OPTS -DCMAKE_INSTALL_RPATH=%{boost_rpath}"
%endif

%if "%{?boost_library}" != ""
# Boost_NO_BOOST_CMAKE=ON  - disable search for cmake
# Boost_NO_SYSTEM_PATHS=ON - only search in specified locations
CMAKE_OPTS="$CMAKE_OPTS
 -DBoost_NO_BOOST_CMAKE=TRUE \
 -DBoost_NO_SYSTEM_PATHS=TRUE \
 -DBOOST_LIBRARYDIR=%{_libdir}/%{boost_library} \
 -DBOOST_INCLUDEDIR=/usr/include/%{boost_library} \
 -DBoost_ADDITIONAL_VERSIONS='%{boost_version};%{boost_version}.0'"
%endif

%if 0%{?use_systemd}
CMAKE_OPTS="$CMAKE_OPTS -DUSE_SYSTEMD=ON"
%endif

%if "%{?_buildhost}" != ""
CMAKE_OPTS="$CMAKE_OPTS -DICINGA2_BUILD_HOST_NAME:STRING=%_buildhost"
%endif

%{?scl_enable} cmake $CMAKE_OPTS -DCMAKE_C_FLAGS:STRING="%{optflags} %{?march_flag}" -DCMAKE_CXX_FLAGS:STRING="%{optflags} %{?march_flag}" .

%{?scl_enable} make %{?_smp_mflags}

%if 0%{?use_selinux}
cd tools/selinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv %{selinux_modulename}.pp %{selinux_modulename}.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -
%endif

%install
%{?scl_enable} make install \
  DESTDIR="%{buildroot}"

# install custom limits.conf for systemd
%if 0%{?configure_systemd_limits}
# for > 2.8 or > 2.7.2
install -D -m 0644 etc/initsystem/icinga2.service.limits.conf %{buildroot}/etc/systemd/system/%{name}.service.d/limits.conf
%endif

# remove features-enabled symlinks
rm -f %{buildroot}/%{_sysconfdir}/%{name}/features-enabled/*.conf

# enable suse rc links
%if "%{_vendor}" == "suse"
%if 0%{?use_systemd}
  ln -sf /usr/sbin/service %{buildroot}%{_sbindir}/rc%{name}
%else
  ln -sf ../../%{_initrddir}/%{name} "%{buildroot}%{_sbindir}/rc%{name}"
%endif
mkdir -p "%{buildroot}%{_fillupdir}/"
mv "%{buildroot}%{_sysconfdir}/sysconfig/%{name}" "%{buildroot}%{_fillupdir}/sysconfig.%{name}"
%endif

%if 0%{?use_selinux}
cd tools/selinux
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 %{selinux_modulename}.pp.${selinuxvariant} \
    %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{selinux_modulename}.pp
done
cd -

# TODO: Fix build problems on Icinga, see https://github.com/Icinga/puppet-icinga_build/issues/11
#/usr/sbin/hardlink -cv %%{buildroot}%%{_datadir}/selinux
%endif

%if "%{_vendor}" == "suse"
install -D -m 0644 tools/syntax/vim/syntax/%{name}.vim %{buildroot}%{_datadir}/vim/site/syntax/%{name}.vim
install -D -m 0644 tools/syntax/vim/ftdetect/%{name}.vim %{buildroot}%{_datadir}/vim/site/ftdetect/%{name}.vim
%else
install -D -m 0644 tools/syntax/vim/syntax/%{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/%{name}.vim
install -D -m 0644 tools/syntax/vim/ftdetect/%{name}.vim %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%endif

install -D -m 0644 tools/syntax/nano/%{name}.nanorc %{buildroot}%{_datadir}/nano/%{name}.nanorc

%check
export CTEST_OUTPUT_ON_FAILURE=1
make test

%pre
%if "%{_vendor}" == "suse"
%if 0%{?use_systemd}
  %service_add_pre %{name}.service
%endif

%verifyscript
%verify_permissions -e %{_rundir}/%{name}/cmd
%endif

%post
# suse
%if "%{_vendor}" == "suse"
%if 0%{?suse_version} >= 1310
%set_permissions %{_rundir}/%{name}/cmd
%endif

%if 0%{?use_systemd}
%fillup_only  %{name}
%service_add_post %{name}.service
%else
%fillup_and_insserv %{name}
%endif

if [ ${1:-0} -eq 1 ]
then
  # initial installation, enable default features
  for feature in checker notification mainlog; do
    ln -sf ../features-available/${feature}.conf %{_sysconfdir}/%{name}/features-enabled/${feature}.conf
  done
fi

exit 0

%else
# rhel

%if 0%{?use_systemd}
%systemd_post %{name}.service
%else
/sbin/chkconfig --add %{name}
%endif

if [ ${1:-0} -eq 1 ]
then
  # initial installation, enable default features
  for feature in checker notification mainlog; do
    ln -sf ../features-available/${feature}.conf %{_sysconfdir}/%{name}/features-enabled/${feature}.conf
  done
fi

exit 0

%endif
# suse/rhel

%preun
# suse
%if "%{_vendor}" == "suse"

%if 0%{?use_systemd}
  %service_del_preun %{name}.service
%else
  %stop_on_removal %{name}
%endif

exit 0

%else
# rhel

%if 0%{?use_systemd}
%systemd_preun %{name}.service
%else
if [ "$1" = "0" ]; then
  /sbin/service %{name} stop > /dev/null 2>&1 || :
  /sbin/chkconfig --del %{name} || :
fi
%endif

exit 0

%endif
# suse / rhel

%postun
# suse
%if "%{_vendor}" == "suse"
%if 0%{?use_systemd}
  %service_del_postun %{name}.service
%else
  %restart_on_update %{name}
  %insserv_cleanup
%endif

%else
# rhel

%if 0%{?use_systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ "$1" -ge  "1" ]; then
  /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif

%endif
# suse / rhel

if [ "$1" = "0" ]; then
  # deinstallation of the package - remove enabled features
  rm -rf %{_sysconfdir}/%{name}/features-enabled
fi

exit 0

%pre common
getent group %{icinga_group} >/dev/null || %{_sbindir}/groupadd -r %{icinga_group}
getent group %{icingacmd_group} >/dev/null || %{_sbindir}/groupadd -r %{icingacmd_group}
getent passwd %{icinga_user} >/dev/null || %{_sbindir}/useradd -c "icinga" -s /sbin/nologin -r -d %{_localstatedir}/spool/%{name} -G %{icingacmd_group} -g %{icinga_group} %{icinga_user}

%if "%{_vendor}" == "suse"
%verifyscript common
%verify_permissions -e %{_rundir}/%{name}/cmd
%endif

%post common
%if "%{_vendor}" == "suse"
%if 0%{?suse_version} >= 1310
%set_permissions %{_rundir}/%{name}/cmd
%endif
%endif

%if %{with mysql}
%post ido-mysql
if [ ${1:-0} -eq 1 ] && [ -e %{_sysconfdir}/%{name}/features-enabled/ido-mysql.conf ]
then
  # initial installation, enable ido-mysql feature
  ln -sf ../features-available/ido-mysql.conf %{_sysconfdir}/%{name}/features-enabled/ido-mysql.conf
fi

exit 0

%postun ido-mysql
if [ "$1" = "0" ]; then
  # deinstallation of the package - remove feature
  rm -f %{_sysconfdir}/%{name}/features-enabled/ido-mysql.conf
fi

exit 0
%endif

%if %{with pgsql}
%post ido-pgsql
if [ ${1:-0} -eq 1 ] && [ -e %{_sysconfdir}/%{name}/features-enabled/ido-pgsql.conf ]
then
  # initial installation, enable ido-pgsql feature
  ln -sf ../features-available/ido-pgsql.conf %{_sysconfdir}/%{name}/features-enabled/ido-pgsql.conf
fi

exit 0

%postun ido-pgsql
if [ "$1" = "0" ]; then
  # deinstallation of the package - remove feature
  rm -f %{_sysconfdir}/%{name}/features-enabled/ido-pgsql.conf
fi

exit 0
%endif

%if 0%{?use_selinux}
%post selinux
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{selinux_modulename}.pp &> /dev/null || :
done
/sbin/fixfiles -R icinga2 restore &> /dev/null || :
/sbin/fixfiles -R icinga2-bin restore &> /dev/null || :
/sbin/fixfiles -R icinga2-common restore &> /dev/null || :
/sbin/semanage port -a -t icinga2_port_t -p tcp 5665 &> /dev/null || :

%postun selinux
if [ $1 -eq 0 ] ; then
  /sbin/semanage port -d -t icinga2_port_t -p tcp 5665 &> /dev/null || :
  for selinuxvariant in %{selinux_variants}
  do
     /usr/sbin/semodule -s ${selinuxvariant} -r %{selinux_modulename} &> /dev/null || :
  done
  /sbin/fixfiles -R icinga2 restore &> /dev/null || :
  /sbin/fixfiles -R icinga2-bin restore &> /dev/null || :
  /sbin/fixfiles -R icinga2-common restore &> /dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%doc COPYING

%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}

%if 0%{?use_systemd}
%attr(644,root,root) %{_unitdir}/%{name}.service
%if 0%{?configure_systemd_limits}
%dir /etc/systemd/system/%{name}.service.d
%attr(644,root,root) %config(noreplace) /etc/systemd/system/%{name}.service.d/limits.conf
%endif
%else
%attr(755,root,root) %config(noreplace) %{_sysconfdir}/init.d/%{name}
%endif
%if "%{_vendor}" == "suse"
%{_sbindir}/rc%{name}
%{_fillupdir}/sysconfig.%{name}
%else
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif

%{_sbindir}/%{name}

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/prepare-dirs
%{_libexecdir}/%{name}/safe-reload

%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}/conf.d
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}/features-available
%exclude %{_sysconfdir}/%{name}/features-available/ido-*.conf
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}/features-enabled
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}/scripts
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_sysconfdir}/%{name}/zones.d
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/constants.conf
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/zones.conf
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/conf.d/*.conf
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/features-available/*.conf
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/zones.d/*
%config(noreplace) %{_sysconfdir}/%{name}/scripts/*

%attr(0750,%{icinga_user},%{icingacmd_group}) %{_localstatedir}/cache/%{name}
%attr(0750,%{icinga_user},%{icingacmd_group}) %dir %{_localstatedir}/log/%{name}
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_localstatedir}/log/%{name}/crash
%attr(0750,%{icinga_user},%{icingacmd_group}) %dir %{_localstatedir}/log/%{name}/compat
%attr(0750,%{icinga_user},%{icingacmd_group}) %dir %{_localstatedir}/log/%{name}/compat/archives
%attr(0750,%{icinga_user},%{icinga_group}) %{_localstatedir}/lib/%{name}
%attr(0750,%{icinga_user},%{icingacmd_group}) %ghost %dir %{_rundir}/%{name}
%attr(2750,%{icinga_user},%{icingacmd_group}) %ghost %{_rundir}/%{name}/cmd
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_localstatedir}/spool/%{name}
%attr(0770,%{icinga_user},%{icinga_group}) %dir %{_localstatedir}/spool/%{name}/perfdata
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_localstatedir}/spool/%{name}/tmp

%files bin
%defattr(-,root,root,-)
%doc COPYING README.md NEWS AUTHORS CHANGELOG.md
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/sbin
%{_libdir}/%{name}/sbin/%{name}
%{plugindir}/check_nscp_api
%{_datadir}/%{name}
%exclude %{_datadir}/%{name}/include
%{_mandir}/man8/%{name}.8.gz

%files common
%defattr(-,root,root,-)
%doc COPYING README.md NEWS AUTHORS CHANGELOG.md tools/syntax
%{_sysconfdir}/bash_completion.d/%{name}
%attr(0750,%{icinga_user},%{icinga_group}) %dir %{_datadir}/%{name}/include
%{_datadir}/%{name}/include/*

%files doc
%defattr(-,root,root,-)
%{_datadir}/doc/%{name}
%docdir %{_datadir}/doc/%{name}

%if %{with mysql}
%files ido-mysql
%defattr(-,root,root,-)
%doc COPYING README.md NEWS AUTHORS CHANGELOG.md
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/features-available/ido-mysql.conf
%{_libdir}/%{name}/libmysql_shim*
%{_datadir}/icinga2-ido-mysql
%endif

%if %{with pgsql}
%files ido-pgsql
%defattr(-,root,root,-)
%doc COPYING README.md NEWS AUTHORS CHANGELOG.md
%config(noreplace) %attr(0640,%{icinga_user},%{icinga_group}) %{_sysconfdir}/%{name}/features-available/ido-pgsql.conf
%{_libdir}/%{name}/libpgsql_shim*
%{_datadir}/icinga2-ido-pgsql
%endif

%if 0%{?use_selinux}
%files selinux
%defattr(-,root,root,0755)
%doc tools/selinux/*
%{_datadir}/selinux/*/%{selinux_modulename}.pp
%endif

%files -n vim-icinga2
%defattr(-,root,root,-)
%if "%{_vendor}" == "suse"
%{_datadir}/vim/site/syntax/%{name}.vim
%{_datadir}/vim/site/ftdetect/%{name}.vim
%else
%{_datadir}/vim/vimfiles/syntax/%{name}.vim
%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%endif

%files -n nano-icinga2
%defattr(-,root,root,-)
%if "%{_vendor}" == "suse"
%dir %{_datadir}/nano
%endif
%{_datadir}/nano/%{name}.nanorc

%changelog
* Thu Aug 11 2022 Alexander Klimov <alexander.klimov@icinga.com> 2.13.5-1
- Update to 2.13.5

* Thu Jun 30 2022 Julian Brost <julian.brost@icinga.com> 2.13.4-1
- Update to 2.13.4

* Thu Apr 14 2022 Julian Brost <julian.brost@icinga.com> 2.13.3-1
- Update to 2.13.3

* Fri Nov 12 2021 Noah Hilverling <noah.hilverling@icinga.com> 2.13.2-1
- Update to 2.13.2

* Wed Aug 18 2021 Noah Hilverling <noah.hilverling@icinga.com> 2.13.1-1
- Update to 2.13.1

* Tue Aug 03 2021 Alexander Klimov <alexander.klimov@icinga.com> 2.13.0-1
- Update to 2.13.0

* Wed Jul 14 2021 Julian Brost <julian.brost@icinga.com> 2.12.5-1
- Update to 2.12.5

* Thu May 27 2021 Julian Brost <julian.brost@icinga.com> 2.12.4-1
- Update to 2.12.4

* Tue Dec 15 2020 Noah Hilverling <noah.hilverling@icinga.com> 2.12.3-1
- Update to 2.12.3

* Mon Nov 23 2020 Julian Brost <julian.brost@icinga.com> 2.12.2-1
- Update to 2.12.2

* Tue Oct 13 2020 Alexander A. Klimov <alexander.klimov@icinga.com> 2.12.1-1
- Update to 2.12.1

* Wed Aug 05 2020 Henrik Triem <henrik.triem@icinga.com> 2.12.0-1
- Update to 2.12.0

* Fri Mar 13 2020 Noah Hilverling <noah.hilverling@icinga.com> 2.12.0-0.rc1.1
- Update to 2.12.0-rc1

* Thu Oct 24 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.11.2-1
- Update to 2.11.2

* Thu Oct 17 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.11.1-1
- Update to 2.11.1

* Thu Sep 19 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.11.0-1
- Update to 2.11.0

* Thu Jul 25 2019 Markus Frosch <markus.frosch@icinga.com> 2.11.0-0.rc1.1
- Prepare pre-release 2.11.0-rc1

* Tue Mar 19 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.10.4-1
- Update to 2.10.4

* Tue Feb 26 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.10.3-2
- Apply quickfix for SLES11

* Tue Feb 26 2019 Michael Friedrich <michael.friedrich@icinga.com> 2.10.3-1
- Update to 2.10.3

* Wed Nov 14 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.10.2-1
- Update to 2.10.2

* Thu Oct 18 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.10.1-1
- Update to 2.10.1

* Thu Oct 11 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.10.0-1
- Update to 2.10.0

* Wed Sep 26 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.9.2-1
- Update to 2.9.2

* Wed Jul 25 2018 Markus Frosch <markus.frosch@icinga.com> 2.10.0-0
- Remove obsoleted icinga2-libs package

* Tue Jul 24 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.9.1-1
- Update to 2.9.1

* Tue Jul 17 2018 Michael Friedrich <michael.friedrich@icinga.com> 2.9.0-1
- Update to 2.9.0

* Wed Apr 25 2018 Jean Flach <jean.flach@icinga.com> 2.8.4-1
- Update to 2.8.4

* Tue Apr 24 2018 Jean Flach <jean.flach@icinga.com> 2.8.3-1
- Update to 2.8.3

* Thu Mar 22 2018 Jean Flach <jean-marcel.flach@icinga.com> 2.8.2-1
- Update to 2.8.2

* Wed Jan 17 2018 Gunnar Beutner <gunnar.beutner@icinga.com> 2.8.1-1
- Update to 2.8.1

* Fri Nov 24 2017 Markus Frosch <markus.frosch@icinga.com> 2.8.0-2
- [SLES] Add systemd limits file
- Add config(noreplace) for the systemd limits file
  (no need to release every OS immediately)
- Update SELinux handling to be compatible to Fedora 27
  (only affecting f27 builds)

* Thu Nov 16 2017 Jean Flach <jean-marcel.flach@icinga.com> 2.8.0-1
- Update to 2.8.0

* Thu Nov 09 2017 Gunnar Beutner <gunnar.beutner@icinga.com> 2.7.2-1
- Update to 2.7.2

* Mon Oct 02 2017 Markus Frosch <markus.frosch@icinga.com> 2.7.1-2
- Fixing systemd limit issues on openSUSE > 42.1

* Thu Sep 21 2017 Michael Friedrich <michael.friedrich@icinga.com> 2.7.1-1
- Update to 2.7.1

* Tue Jun 20 2017 Markus Frosch <markus.frosch@icinga.com> 2.7.0-1
- Update to 2.7.0
