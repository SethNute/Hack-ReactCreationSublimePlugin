<b>Installation:</b>
Clone this repo into your sublime packages directory. This will add the command <code>make_react_files</code>.
Open the <code>config.py</code> file and set <code>BASE_CLOSURE_PATH</code> and <code>BASE_REACT_PATH</code> to the paths of your closure and react component directories, respectively. Make sure they have a following <code>/</code> after the path string. For example, if your closure  directory has the path <code>home/seth/documents/closure</code> you would want <code>BASE_CLOSURE_PATH = "home/seth/documents/closure/"</code> 

Next add your module prefixes as <code>BASE_CLOSURE_MODULE_PREFIX</code> and <code>BASE_REACT_MODULE_PREFIX</code>. For example, if you named your closure modules using the pattern <code>closure.mythings.thing1</code> you would want <code>BASE_CLOSURE_MODULE_PREFIX = "closure."</code>

<b>What it does:</b>
Given a module name and a shortened directory, create skeleton files for the closure + react component pair in the respective component directories.

<b>To use:</b>
You can then run the command via <code>ctrl+shift+r</code> or by right clicking on the sidebar and selecting 'Make New React Files'. 
You can also open the sublime terminal with <code>ctrl+`</code> and enter the command <code>window.run_command('make_react_files')</code>.

Once the command has been run you will be prompted twice. The first prompt asks for the module name you would like these components to have, minus the leading prefixes. (what goes in <code>goog.provide</code>). For example, if you wanted to name these components <code>closure.mythings.FooBar</code> and <code>react.mythings.FooBar</code>, you would enter the string <code>mythings.FooBar</code> in the first prompt.

The second prompt asks you for the filename path of these components, starting from after the base directories. For example, if your closure components will live in <code>closure/mythings/foo_bar.jsx</code> and <code>react/mythings/foo_bar.jsx</code> you would enter <code>mythings/foo_bar.js</code> in this prompt. 

After completing these prompts your two new files will be open in two new sublime tabs.

<b>Capabilites:</b>
Works with sublime text 2, not sure about 3

Can create directories if they do not already exist in the path you want to create a file on

<b>Customization:</b>
If you dislike the sidebar or hot-key changes, remove the <code>Side Bar.sublime-menu</code> file or the <code>Default.sublime-keymap</code> file (for your OS), respectively 

