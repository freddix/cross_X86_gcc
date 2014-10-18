%define		mver	4.9
%define		snap	20140820

Summary:	Cross GNU Compiler Collection for the x86_64 architecture
Name:		cross_X86_gcc
Version:	4.9.2
Release:	1
License:	GPL v3+
Group:		Development/Languages
#Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{version}/gcc-%{version}.tar.bz2
Source0:	ftp://gcc.gnu.org/pub/gcc/snapshots/%{mver}-%{snap}/gcc-%{mver}-%{snap}.tar.bz2
# Source0-md5:	f801935766e791a71efe23e037f7e058
Source1:	http://www.mpfr.org/mpfr-current/mpfr-3.1.2.tar.xz
# Source1-md5:	e3d203d188b8fe60bb6578dd3152e05c
Source2:	ftp://ftp.gnu.org/gnu/gmp/gmp-6.0.0a.tar.xz
# Source2-md5:	1e6da4e434553d2811437aa42c7f7c76
Source3:	http://multiprecision.org/mpc/download/mpc-1.0.1.tar.gz
# Source3-md5:	b32a2e1a3daa392372fbd586d1ed3679
URL:		http://gcc.gnu.org/
BuildConflicts:	gmp-devel
BuildConflicts:	mpc-devel
BuildConflicts:	mpfr-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	chrpath
BuildRequires:	coreutils
BuildRequires:	cross_X86_binutils
BuildRequires:	flex
BuildRequires:	texinfo
Requires:	cross_X86_binutils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/usr/lib
%define		_libexecdir	%{_libdir}
%define		_slibdir	%{_libdir}

%define         target          i586-freddix-linux
%define         arch            %{_prefix}/%{target}
%define         gccarch         %{_libdir}/gcc/%{target}
%define         gcclib          %{gccarch}/%{version}

%define         _noautostrip    .*/lib.*\\.a

%define		debug_package	%{nil}

%description
Cross GNU Compiler Collection for the x86_64 architecture.

%prep
%setup -qn gcc-%{mver}-%{snap}

# undefined reference to `__stack_chk_guard'
sed -i '/k prot/agcc_cv_libc_provides_ssp=yes' gcc/configure

tar -xf %{SOURCE1}
mv mpfr-3.1.2 mpfr
tar -xf %{SOURCE2}
mv gmp-6.0.0 gmp
tar -xf %{SOURCE3}
mv mpc-1.0.1 mpc

%build
install -d obj-%{target}
cd obj-%{target}

TEXCONFIG=false				\
CFLAGS="%{rpmcflags}"			\
LDFLAGS="%{rpmldflags}"			\
../configure				\
	--build=%{_build}		\
	--host=%{_host}			\
	--target=%{target}		\
	--bindir=%{_bindir}		\
	--infodir=%{_infodir} 		\
	--libdir=%{_libdir}		\
	--libexecdir=%{_libexecdir}	\
	--mandir=%{_mandir}		\
	--prefix=%{_prefix}		\
	--sbindir=%{_sbindir}		\
	--with-mpfr-include=$(pwd)/../mpfr/src	\
	--with-mpfr-lib=$(pwd)/mpfr/src/.libs	\
	--disable-decimal-float		\
	--disable-libatomic		\
	--disable-libcilkrts		\
	--disable-libgomp		\
	--disable-libitm		\
	--disable-libquadmath		\
	--disable-libsanitizer		\
	--disable-libssp		\
	--disable-libstdc++-v3		\
	--disable-libvtv		\
	--disable-multilib		\
	--disable-nls			\
	--disable-shared		\
	--disable-threads		\
	--enable-languages=c,c++
cd ..

%{__make} -C obj-%{target} \
	CFLAGS_FOR_TARGET="-O2"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}}

%{__make} -C obj-%{target} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install obj-%{target}/gcc/specs $RPM_BUILD_ROOT%{gcclib}
rm -f $RPM_BUILD_ROOT%{_libdir}/libiberty.a

gccdir=$RPM_BUILD_ROOT%{gcclib}
mv $gccdir/include-fixed/{limits,syslimits}.h $gccdir/include
rm -r $gccdir/include-fixed
rm -r $gccdir/install-tools

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{gccarch}
%dir %{gcclib}
%dir %{gcclib}/include
%attr(755,root,root) %{_bindir}/%{target}-c++
%attr(755,root,root) %{_bindir}/%{target}-cpp
%attr(755,root,root) %{_bindir}/%{target}-g++
%attr(755,root,root) %{_bindir}/%{target}-gcc*
%attr(755,root,root) %{_bindir}/%{target}-gcov
%attr(755,root,root) %{gcclib}/*.a
%attr(755,root,root) %{gcclib}/*.o
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/cc1plus
%attr(755,root,root) %{gcclib}/collect2
%attr(755,root,root) %{gcclib}/liblto_plugin.so*
%attr(755,root,root) %{gcclib}/lto-wrapper
%attr(755,root,root) %{gcclib}/lto1
%{gcclib}/plugin
%{gcclib}/include/*.h
%{gcclib}/specs

%{_mandir}/man1/%{target}-cpp.1*
%{_mandir}/man1/%{target}-gcc.1*
%{_mandir}/man1/%{target}-gcov.1*

