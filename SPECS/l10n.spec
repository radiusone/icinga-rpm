# Icinga L10n | (c) 2020 Icinga GmbH

%define revision    1
%define basedir     %{_datadir}/icinga-L10n

%if 0%{?el5}%{?el6}%{?amzn}%{?suse_version}
%define use_selinux 0
%else
%define use_selinux 1
%define selinux_variants mls targeted
%endif


Name:       icinga-l10n
Version:    1.2.0
Release:    %{revision}%{?dist}
Summary:    Icinga L10n
License:    GPLv2+
URL:        https://icinga.com
Source0:    https://github.com/Icinga/L10n/archive/v%{version}.tar.gz
BuildArch:  noarch
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}
Packager:   Icinga GmbH <info@icinga.com>


%prep
%setup -q -n L10n-%{version}
cp -r %{_topdir}/../selinux selinux

%build
%if 0%{?use_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}
do
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  mv icinga-l10n.pp icinga-l10n.pp.${selinuxvariant}
  make NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -
%endif

%install
mkdir -p %{buildroot}/%{basedir}
cp *.md %{buildroot}/%{basedir}
cp COPYING %{buildroot}/%{basedir}
cp -prv locale %{buildroot}/%{basedir}
find %{buildroot}/%{basedir}/locale -name *.po -delete
%if 0%{?use_selinux}
cd selinux
for selinuxvariant in %{selinux_variants}
do
  install -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  install -p -m 644 icinga-l10n.pp.${selinuxvariant} %{buildroot}%{_datadir}/selinux/${selinuxvariant}/icinga-l10n.pp
done
cd -
%endif

%clean
rm -rf %{buildroot}


# Main package
%description
L10n (short for Localization) provides all translations available for Icinga.

%files
%defattr(-,root,root)
%{basedir}
%doc README.md
%doc CONTRIBUTING.md


# Selinux package
%if 0%{?use_selinux}

%package selinux
Summary:            SELinux policy for Icinga L10n
BuildRequires:      checkpolicy, selinux-policy-devel
Requires:           %{name} = %{version}-%{release}
Requires(post):     policycoreutils
Requires(postun):   policycoreutils

%description selinux
SELinux policy for Icinga L10n

%post selinux
for selinuxvariant in %{selinux_variants}
do
  %{_sbindir}/semodule -s ${selinuxvariant} -i %{_datadir}/selinux/${selinuxvariant}/icinga-l10n.pp &> /dev/null || :
done
%{_sbindir}/restorecon -R %{basedir} &> /dev/null || :

%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
     %{_sbindir}/semodule -s ${selinuxvariant} -r icinga-l10n &> /dev/null || :
  done
  [ -d %{basedir} ] && %{_sbindir}/restorecon -R %{basedir} &> /dev/null || :
fi

%files selinux
%defattr(-,root,root,0755)
%doc selinux/*
%{_datadir}/selinux/*/icinga-l10n.pp

%endif


%changelog
* Fri Jul 15 2022 Johannes Meyer <johannes.meyer@icinga.com> 1.2.0-1
- Version 1.2.0

* Wed Jul 7 2021 Johannes Meyer <johannes.meyer@icinga.com> 1.1.0-1
- Updated German translation (de_DE)
- Updated Russian translation (ru_RU)
- Updated Ukrainian translation (uk_UA)
- Added Spanish (Argentina) translation (es_AR)

* Mon Jun 8 2020 Johannes Meyer <johannes.meyer@icinga.com> 1.0.0-1
- Initial release

