
export PYTHONPATH=`pwd`/code
export THIS=`pwd`
function whisper { python -c "import whisper;whisper.add('$1')" ; }
function _whisper_feeds () { COMPREPLY=( $(compgen -W "`ls /home/alan/projects/_/2017/Whisper/feeds`" $2) ) ; }
#complete -o nospace -F _whisper_feeds whisper
complete -F _whisper_feeds whisper
