node 'vagrant-trusty64' {

    package { 'pip':
        ensure   => latest,
        provider => 'pip',
        require  => Package['python-pip'],
    }

    package { 'python-pip':
        ensure => present
    }
}
