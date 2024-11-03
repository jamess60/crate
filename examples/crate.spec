Name:		crate
Version:	1.1
Release:	0%{?dist}
Summary:	CRATE (Container Recovery and Archival ToolsEt)

License:	None
URL:		https://github.com/jamess60/crate
Vendor:		james_s60
Packager:	james_s60

BuildArch:	noarch

Requires:	python3, python3-paramiko, python3-colorama

%define Crate_PATH /usr/share/crate

%description
A package to deploy crate on a per host basis utilising backup/recover-local modes.


%global __os_install_post %{nil}

%{!?python_disable_bytecompile:%global python_disable_bytecompile 0}
%{python_disable_bytecompile: %global __python /usr/bin/python -E}


%install
#rm -rf %{buildroot}
mkdir -p %{buildroot}%{Crate_PATH}
mkdir -p %{buildroot}%{Crate_PATH}/conf
cp -r %{_sourcedir}/crate/src %{buildroot}%{Crate_PATH}
cp -a %{_sourcedir}/crate/conf/config.ini %{buildroot}%{Crate_PATH}/conf

mkdir -p %{buildroot}/etc/cron.d
cp %{_sourcedir}/crate/conf/crate.cron %{buildroot}/etc/cron.d/crate.cron

#%clean
#rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
/etc/cron.d/crate.cron
%attr(775,yourusername,yourusername)%{Crate_PATH}

%doc



%changelog
