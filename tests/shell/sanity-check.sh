#!/bin/bash


RET=0
set -o pipefail

check_file_presence()
{
    echo -n "Check file presence: "
    RESULT="OK"
    # all JSON files should have a LICENSE file
    for lf in `find var/licenses -name "*.json"`; 
    do 
        LICENSE_FILE=`echo $lf | sed 's/\.json/\.LICENSE/g'` ; 
        ls $LICENSE_FILE > /dev/null
        if [ $? -ne 0 ]
        then
            echo "FAIL: $LICENSE_FILE missing"
            RET=$(( $RET + 1 ))
            RESULT=" FAIL"

        fi
        jq . $lf > /dev/null
        if [ $? -ne 0 ]
        then
            echo "FAIL: $lf not in JSON format"
            RET=$(( $RET + 1 ))
            RESULT=" FAIL"
        fi
    done
    
    # all LICENSE files should have a JSON file
    for lf in `find var/licenses -name "*.LICENSE"`; 
    do JSON_FILE=`echo $lf | sed 's/\.LICENSE/\.json/g'` ; 
       ls $JSON_FILE > /dev/null
       if [ $? -ne 0 ]
       then
           echo "FAIL $lf file missing"
           RET=$(( $RET + 1 ))
           RESULT=" FAIL"
       fi
    done
    echo "$RESULT"
}

check_schema()
{
    # Make sure schema is valid JSON
    echo -n "License schema: " ; 
    jq . var/license_schema.json > /dev/null 
    if [ $? -ne 0 ]
    then
        echo FAIL;
        RET=$(( $RET + 1 ))
    fi
    echo "OK" 
}

check_presence()
{
    LICENSE=$1
    FILE=var/licenses/$LICENSE.json

    REG_EXP_PRESENCE="$2"
    REG_EXP_UNPRESENCE="$3"

    _RET="OK"
    
    # check presence
    #echo "cat $FILE | jq  -r .aliases[] | grep -v $REG_EXP_PRESENCE )" | bash
    PRESENT=$(echo "cat $FILE | jq  -r .aliases[] | grep -v $REG_EXP_PRESENCE" | bash )
    echo -n "$LICENSE: "
    if [ "$PRESENT" != "" ]
    then
        echo "FAIL"
        echo " * cause: Incorrectly present in $FILE"
        echo " --------------------------"
        echo "$PRESENT"
        echo " --------------------------"
        RET=$(( $RET + 1 ))
        _RET="FAIL"
    fi


    # check unpresence
    if [ "$REG_EXP_UNPRESENCE" != "" ]
    then
        
        UNPRESENT=$(echo "cat $FILE | jq  -r .aliases[] | grep $REG_EXP_UNPRESENCE" | bash )
        if [ "$UNPRESENT" != "" ]
        then
            echo "FAIL"
            echo " * cause: Incorrectly not present in $FILE"
            echo " --------------------------"
            echo "$UNPRESENT"
            echo " --------------------------"
            RET=$(( $RET + 1 ))
            _RET="FAIL"
        fi
    fi
    
    if [ "$_RET" = "OK" ]
    then
        echo OK
    fi
}

#check_file_presence
#check_schema


ZERO_BSD_PRESENT=" -e 0BSD -i -e zero "
BSD2_PRESENT=" -e 2 -i -e two -e simplified -e freebsd "
BSD3_PRESENT=" -e 3 -i -e new -e modified -e revised -e three -e 'no advertising' "
BSD4_PRESENT=" -e 4 -i -e 'BSD with advertising' -e original "

check_presence Apache-2.0 " -e 2" "-e 1"
check_presence Apache-1.0 " -e 1.0" "-e 2 -e 1.1"
check_presence Apache-1.1 " -e 1.1" "-e 2 -e 1.0"
check_presence MPL-2.0 " -e 2" "-e 1"
check_presence MPL-1.0 " -e 1.0" "-e 2 -e 1.1"
check_presence MPL-1.1 " -e 1.1" "-e 2 -e 1.0"
check_presence 0BSD "$ZERO_BSD_PRESENT" "$BSD3_PRESENT $BSD2_PRESENT "
check_presence BSD-2-Clause "$BSD2_PRESENT" "$ZERO_BSD_PRESENT $BSD3_PRESENT "
check_presence BSD-3-Clause "$BSD3_PRESENT" "$ZERO_BSD_PRESENT $BSD2_PRESENT"
check_presence BSD-4-Clause "$BSD4_PRESENT" " $ZERO_BSD_PRESENT $BSD2_PRESENT $BSD3_PRESENT"

exit $RET
