# Icinga SELinux Common | (c) 2022 Icinga GmbH | GPLv2+

%define revision 1

%global debug_package %{nil}

Summary:          Common SELinux policies for all Icinga Components
%if "%{_vendor}" == "suse"
License:          GPL-2.0-or-later
%else
License:          GPLv2+
%endif # suse
Group:            System/Base
Name:             icinga-selinux-common
Version:          1.0.0
Release:          %{revision}%{?dist}
Url:              https://www.icinga.com

BuildRoot:        %{_tmppath}/%{name}-%{version}-build
BuildArch:        noarch
%if 0%{?fedora} >= 27 || 0%{?rhel} >= 8
Requires(post):   policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils
%else
Requires(post):   policycoreutils-python
Requires(postun): policycoreutils-python
%endif

%description
Common SELinux policies for all Icinga Components

%prep
%build
%install

%post
/sbin/semanage port -a -t redis_port_t -p tcp 6380 &> /dev/null
exit 0

%postun
if [ $1 -eq 0 ] ; then
    /sbin/semanage port -d -t redis_port_t -p tcp 6380 &> /dev/null
fi
exit 0

%files

%changelog
* Thu Jul 28 2022 Yonas Habteab <yonas.habteab@icinga.com> 1.0.0-1
- Initial commit
