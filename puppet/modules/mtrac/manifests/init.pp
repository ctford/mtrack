class mtrac {
  package { "python-pip":
    ensure => present,
  }

  $django = ["django", "django-extensions", "django-nose", "django-tablib",
             "django-uni-form", "djappsettings", "django-mptt", "django-guardian",
             "django-digest", "django-celery"]

  package { $django:
    ensure => present,
    provider => pip,
  }

  package { "south":
    ensure => present,
    provider => pip,
  }

  $misc = ["python-dateutil", "pytz", "virtualenv", "xlrd", "python-memcached"]

  package { $misc:
    ensure => present,
    provider => pip,
  }
}
