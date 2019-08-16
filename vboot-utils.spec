%define _default_patch_fuzz 2
%define gitshort 2cc35b0
%define _disable_lto 1

Name:		vboot-utils
Version:	20180531
Release:	2.git%{gitshort}%{?dist}
Summary:	Verified Boot Utility from Chromium OS
License:	BSD
URL:		https://chromium.googlesource.com/chromiumos/platform/vboot_reference

ExclusiveArch:	%{arm} aarch64 %{ix86} %{x86_64}

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  git clone https://git.chromium.org/git/chromiumos/platform/vboot_reference.git
#  cd vboot_reference/
#  git archive --format=tar --prefix=vboot-utils-a1c5f7c/ a1c5f7c | xz > vboot-utils-a1c5f7c.tar.xz
Source0:	%{name}-%{gitshort}.tar.xz

## Patch0 disabled static building.
Patch0:		vboot-utils-00-disable-static-linking.patch

#make sure get the rpmbuild flags passed in
Patch1:		vboot-utils-cflags.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:	openssl-devel
BuildRequires:	trousers-devel
BuildRequires:	yaml-devel
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(liblzma)

# for the test scripts
BuildRequires:	python2

%description
Verified boot is a collection of utilities helpful for chromebook computer.
Pack and sign the kernel, manage gpt partitions.


%prep
%setup -q -n %{name}-%{gitshort}
%patch0 -p1 -b .nostatic
%patch1 -p1 -b .cflags
sed -i 's/-Werror//g' Makefile


%build
export CC=gcc

%ifarch %{armx}
%global ARCH arm
%endif

%ifarch %{x86_64}
%global ARCH x86_64
%endif

%ifarch i686
%global ARCH i386
%endif

make V=1 ARCH=%{ARCH} COMMON_FLAGS="%{optflags}"

%install
make install V=1 DESTDIR=%{buildroot}/usr ARCH=%{ARCH} COMMON_FLAGS="%{optflags}"

# Remove unneeded build artifacts
rm -rf %{buildroot}/usr/lib/pkgconfig/
rm -rf %{buildroot}/usr/default/

## Tests are enabled but ignored (will not break the build).
## This is because tests fail in a chroot (mock) but work otherwise.
%check
make runtests || true


%files
%license LICENSE
%doc README
%{_bindir}/*
