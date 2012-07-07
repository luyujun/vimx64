" 文件是否加载
let g:autoCommandIsLoad=0
" 脚本目录
let s:scriptDir=expand('<sfile>:h')
" 调试模式
let s:isDebug=1

fu! AutoCommand()
  " 保存文件
  silent up
  " 如果文件未加载则加载
  if !g:autoCommandIsLoad || s:isDebug == 1 | call AutoCommand#load() | en
  " 保存缓冲区文件名
  if !exists('w:fullFileName') || s:isDebug == 1 | let w:fullFileName = expand('%:p') | en
  " 保存命令
  if !exists('w:commandCache') || s:isDebug == 1 | let w:commandCache = '' | en
  " 执行命令
  py runCommand()
endf

" 加载autoCommand.py
fu! AutoCommand#load()
  "echo "pyfile ".s:scriptDir."/autoCommand/autoCommand.py"
  exec "pyfile ".s:scriptDir."/autoCommand/autoCommand.py"
  let g:autoCommandIsLoad=1
endf

" 重置缓存
fu! AutoCommand#flush()
  call AutoCommand#load()
  if exists('w:fullFileName') | unlet w:fullFileName | en
  if exists('w:commandCache') | unlet w:commandCache | en
endf

" 绑定事件
fu! AutoCommand#bind()
  no <silent> <buffer> <C-s> :call AutoCommand()<CR>
  vno <silent> <buffer> <C-s> <C-C>:call AutoCommand()<CR>
  ino <silent> <buffer> <C-s> <C-O>:call AutoCommand()<CR>
endf

" 初始化配置文件
fu! AutoCommand#init()
  " 如果文件未加载则加载
  if !g:autoCommandIsLoad | call AutoCommand#load() | en
  let s:cwd = getcwd()
  let s:dir=input("create config ".s:cwd."(yN):")
  if s:dir == 'y'
    py createConfigFile()
    echo "success"
  else
    echo "abort"
  en
endf

" 默认命令
fu! AutoCommand#getCommand(type)
  if a:type == ".haml"
    let s:retText = "haml --no-escape-arrts -q #{$fileName}.haml #{$fileName}.html"
  elsei a:type == ".sass"
    let s:retText = "sass #{$fileName}.sass #{$fileName}.css"
  elsei a:type == ".less"
    let s:retText = "lessc #{$fileName}.less>#{$fileName}.css"
  elsei a:type == ".coffee"
    let s:retText = "coffee -pb #{$fileName}.coffee #{$fileName}.js"
  en
endf

" 设置自启动
au FileType haml call AutoCommand#bind()
au FileType sass call AutoCommand#bind()
au FileType scss call AutoCommand#bind()
au FileType coffee call AutoCommand#bind()
"au FileType less call AutoCommand#bind()
"au FileType coffee call AutoCommand#bind()
