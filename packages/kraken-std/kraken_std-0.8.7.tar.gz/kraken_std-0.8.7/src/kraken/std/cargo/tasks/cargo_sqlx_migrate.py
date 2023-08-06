from __future__ import annotations

import os
import subprocess as sp
from pathlib import Path
from typing import List

from kraken.core import Task, TaskStatus
from kraken.core.api import Property


class CargoSqlxMigrateTask(Task):
    database_url: Property[str]
    migrations: Property[Path]
    verify_metadata: Property[bool] = Property.default(False)

    def execute(self) -> TaskStatus:
        result = self.db_create()
        if result.is_not_ok():
            return result

        result = self.migrate_run()
        if result.is_not_ok():
            return result

        if self.verify_metadata.get():
            result = self.prepare_check()
            if result.is_not_ok():
                return result

        return TaskStatus.succeeded()

    def db_create(self) -> TaskStatus:
        return self._execute_command(["db", "create"])

    def migrate_run(self) -> TaskStatus:
        arguments = ["migrate", "run"]
        if self.migrations.is_filled():
            arguments.extend(["--source", str(self.migrations.get().absolute())])

        return self._execute_command(arguments)

    def prepare_check(self) -> TaskStatus:
        return self._execute_command(["prepare", "--check"])

    def _execute_command(self, arguments: List[str]) -> TaskStatus:
        command = ["cargo", "sqlx", *arguments]
        if self.database_url.is_filled():
            command.extend(["--database-url", self.database_url.get()])

        result = sp.call(command, cwd=self.project.directory, env={**os.environ})

        return TaskStatus.from_exit_code(command, result)

    def get_description(self) -> str | None:
        return """Apply SQL migrations using cargo sqlx. If the database URL is not provided, it will default to the
        environment variable DATABASE_URL. If the database does not exist, it will be created.

        If verify_metadata=True, sqlx will also verify sqlx metadata is up-to-date with migrations and queries.
        """
