from django.db import migrations


SQL_CREATE_TASKMODEL = r"""
CREATE TABLE IF NOT EXISTS `core_taskmodel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `test_code` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
"""


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_recreate_taskmodel_if_missing"),
    ]

    operations = [
        migrations.RunSQL(SQL_CREATE_TASKMODEL, migrations.RunSQL.noop),
    ]
