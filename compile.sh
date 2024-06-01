for dirname in en ja; do
    cd $dirname
    for file in $(ls sunao_type_*.tex); do
        echo $file
        latexmk -pdfdvi $file
    done
    # latexmk -c
    cd ..
done
