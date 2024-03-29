#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	SSR packets scheduler (Simple Round Robin)
Summary(pl.UTF-8):	Moduł szeregujący pakiety SRR (prosty algorytm karuzelowy)
Name:		kernel%{_alt_kernel}-net-sch_srr
Version:	0.4.2
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://mordor.strace.net/sched-srr/sch_srr.v%{version}.tgz
# Source0-md5:	b51172937997920bfcc1381340cf9de6
URL:		http://mordor.strace.net/sched-srr/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains SRR packets scheduler (Simple Round Robin).

Simple Round Robin packets schedules - this is the schedules of
packets for the Linux operating system with kernels 2.4 or 2.6. Its
purpose is the simply round robin distribution of the resources of the
allocated bandwidth between its users. It works as follows: the
internal queue of scheduler is divided into the given number of
virtual queues (slots). Each slot, in turn, has hard limited number of
packets located in it. Internal classifier distributes the entering in
scheduler packets along the slots, being based either on source IP
address or on destination IP address. With the selection of packet
from the scheduler, the slots will be processed cyclically, which will
ensure more or less uniform distribution.

%description -l pl.UTF-8
Ten pakiet zawiera moduł szeregujący pakiety SRR (Simple Round Robin).

Prosty algorytm karuzelowy przeznaczony dla Linuksa z jądrem 2.4 lub
2.6. Jego zadaniem jest zarządzanie dostępnym pasmem pomiędzy
wszystkich użytkowników. Prosty algorytm karuzelowy (SRR - Simple
Round Robin) działa w następujący sposób: kolejka wewnętrzna modułu
szeregującego jest dzielona na zadaną liczbę wirtualnych kolejek
(slotów). Z kolei każdy slot posiada ściśle ograniczoną liczbę
pakietów. Wewnętrzny klasyfikator dzieli wchodzące pakiety pomiędzy
sloty używając do tego celu źródłowego lub docelowego adresu IP. Sloty
przetwarzane są karuzelowo (cyklicznie) co zapewnia mniej lub bardziej
sprawiedliwą dystrybucję pakietów.

%prep
%setup -q -n sch_srr.v%{version}

cat > Makefile <<'EOF'
obj-m := sch_srr.o
CFLAGS += -DKERNEL26
EOF

%build
%build_kernel_modules  -m sch_srr

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m sch_srr -d kernel/net/sched

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/net/sched/sch_srr*.ko*
