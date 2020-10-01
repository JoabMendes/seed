require 'simplecov'
require 'coveralls'

SimpleCov.formatter = Coveralls::SimpleCov::Formatter
SimpleCov.start do
   add_filter 'docs'
   add_filter 'seed/vcs'
   add_filter '*__init__.py'
end
