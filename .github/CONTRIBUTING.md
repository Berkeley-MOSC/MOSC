This is a more terse version of my description of the [entire Git
workflow](https://nicholas-fong.com/2015/11/20/git-workflows.html).

* Regardless of what you're working on, all non-merge commits should be made on a
  feature branch
* Commit messages, although they do not have to follow the
  [standards](https://nicholas-fong.com/2015/11/30/commit-messages.html) many
  open source codebases abide by,
* To avoid extraneous merge commits, all pulls should be `pull --rebase`s
* Before anything is merged into `master`, the branch must be rebased off of
  the current `HEAD` of `master`
* Merging is done with the `--no-ff` flag, so pull requests should not be merged
  in via the GitHub UI
* Feature branches are deleted once they've been merged into `master` and
  successfully pushed back up to GitHub
