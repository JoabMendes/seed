import re
from pipes import quote

from seed.exceptions import ShellCommandError
from seed.utilities import run_command
from seed.vcs import BaseVcs


class GitVcs(BaseVcs):
    name = "git"

    def get_suitability(self):
        try:
            run_command("git status")
        except ShellCommandError:
            return 0

        return 1

    def get_changes(self, since_version):
        log_range = "%s..HEAD" % self.make_tag_name(since_version)
        commits = run_command("git log --pretty=short %s" % quote(log_range))

        return self.parse_log_messages(commits)

    def commit(self, message, files):
        quoted_files = " ".join(map(quote, files))
        run_command("git add %s" % quoted_files)
        run_command("git commit -m %s %s" % (quote(message), quoted_files))

    def tag(self, version):
        name = self.make_tag_name(version)
        run_command("git tag %s" % quote(name))

    @staticmethod
    def push():
        run_command("git push")
        run_command("git push --tags")

    @staticmethod
    def add(file_path):
        run_command("git add %s" % quote(file_path))

    def get_download_url(self, version):
        return None

    @staticmethod
    def parse_log_messages(text):
        """Will parse git log messages in the 'short' format"""
        regex = r"commit ([0-9a-f]+)\nAuthor: (.*?)\n\n(.*?)(?:\n\n|$)"
        messages = re.findall(regex, text, re.DOTALL)

        parsed = []
        for commit, author, message in messages:
            parsed.append((
                commit[:10],
                # Remove email address if present
                re.sub(r"\s*<.*?>", "", author),
                message.strip()
            ))
        return parsed


GitVcs()
