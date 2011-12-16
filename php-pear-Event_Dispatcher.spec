%define		_class		Event
%define		_subclass	Dispatcher
%define		upstream_name	%{_class}_%{_subclass}

%define		_requires_exceptions pear(PHPUnit.php)

Name:		php-pear-%{upstream_name}
Version:	1.1.0
Release:	%mkrel 5
Summary:	Dispatch notifications using PHP callbacks
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/Event_Dispatcher/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tar.bz2
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	php-pear
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The Event_Dispatcher acts as a notification dispatch table. It is used
to notify other objects of interesting things. This information is
encapsulated in Event_Notification objects. Client objects register
themselves with the Event_Dispatcher as observers of specific
notifications posted by other objects. When an event occurs, an object
posts an appropriate notification to the Event_Dispatcher. The
Event_Dispatcher dispatches a message to each registered observer,
passing the notification as the sole argument.


%prep
%setup -q -c
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{upstream_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%doc %{upstream_name}-%{version}/examples
%{_datadir}/pear/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml
