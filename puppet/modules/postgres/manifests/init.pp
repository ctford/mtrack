class postgres {

  package { "postgresql":
    ensure => present,
  }

  service { "postgresql":
    ensure => running,
  }
}
