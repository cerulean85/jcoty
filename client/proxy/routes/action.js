var express = require("express")
var router = express.Router();
const config = require("../config");
const cors = require("cors");
const grpc = require("../routes/stub");
// const query = require("../routes/query");
const query = require("../routes/sqlite");
const util = require("../routes/util");


router.get('/', function(req, res) {
    res.send("Welcome!!" + util.currentDatetime())
});

router.post('/echo', function(req, res) {
   grpc.stub.echo(res, req, function (err, proto_res) {
       if (grpc.existReponsedResult(proto_res, err))
           return res.send(proto_res)
   })
});

function generateKeywords(keywords, key_opts) {
    let currentKeywordIndex = 0

    const split_keywords = keywords.length === 1 ? keywords[0] : keywords.split(',')
    const split_key_opts = key_opts.length === 1 ? key_opts[0] : key_opts.split(',')

    let currentKeywords = [split_keywords[currentKeywordIndex]]
    for(var index=0; index<split_key_opts.length; index++) {
        currentKeywordIndex++;
        const targetKeyword = split_keywords[currentKeywordIndex]
        const opt = split_key_opts[index]
        let refreshedKeywords = [];
        if(opt === "AND") {
            for(var jdex=0; jdex<currentKeywords.length; jdex++) {
                refreshedKeywords.push(currentKeywords[jdex] + ' ' + targetKeyword)
            }
            currentKeywords = refreshedKeywords;
        }
        if(opt === "OR") {
            console.log(opt)
            for(var jdex=0; jdex<currentKeywords.length; jdex++) {
                refreshedKeywords.push(currentKeywords[jdex])
                refreshedKeywords.push(currentKeywords[jdex] + ' ' + targetKeyword)
            }
            currentKeywords = refreshedKeywords;
        }
    }

    return currentKeywords
}

router.post("/get_work_group_list", function(req, res){
    query.query_select({
        "addr": "/get_work_group_list", "call_res": res, "reverse": false, "res_send": false,
        "sql": `SELECT * FROM work_groups WHERE deleted = 0`,
        "emit": function (result) {
            let workGroupList = []
            var timestamp = new Date().getTime();

            for (const workGroup of result) {

                const updateTimeDTForm = util.stringToDatetime(workGroup.update_time)
                var report = ''
                try {
                    if (workGroup.report != null)
                        report = JSON.parse(workGroup.report)

                } catch (e) {
                    console.error(e)
                }

                workGroupList.push({
                    "id": workGroup.id,
                    "title": workGroup.title,
                    "keywords": workGroup.keywords,
                    "channels": workGroup.channels,
                    "start_date": workGroup.start_date,
                    "end_date": workGroup.end_date,
                    "work_state": workGroup.work_state,
                    "started": workGroup.update_time,
                    "update_time": (timestamp - updateTimeDTForm.getTime()) / 1000,
                    "report": report
                })
            }
            res.send({
                err: undefined,
                totalCount: workGroupList.length,
                list: workGroupList
            })
            console.log(workGroupList)
        }
    });
})

router.post("/enroll_works", function(req, res){
    query.query_insert({
        "addr": "/enroll_works", "call_res": res, "reverse": false, "res_send": true,
        "sql": `INSERT INTO work_groups(title, keywords, channels, start_date, end_date, work_state, update_time) 
                            VALUES(
                                '${req.body.title}', '${req.body.keywords}', '${req.body.channels}', 
                                '${req.body.start_dt}', '${req.body.end_dt}', 'waiting', '${util.currentDatetime()}')`,
        "emit": function (result) { }
    });
})

router.post("/attach_work", function(req, res){
    console.log(req.body.id)
    query.query_insert({
        "addr": "/attach_work", "call_res": res, "reverse": false, "res_send": true,
        "sql": `UPDATE work_groups SET 
                    work_state = 'attached', 
                    update_time = '${util.currentDatetime()}'
                    WHERE id = ${req.body.id}`,
        "emit": function (result) {
        }
    });
})

router.post("/stop_work", function(req, res){
    query.query_insert({
        "addr": "/stop_work", "call_res": res, "reverse": false, "res_send": true,
        "sql": `UPDATE work_groups SET 
                    work_state = 'stopped', 
                    update_time = '${util.currentDatetime()}'
                    WHERE id = ${req.body.id}`,
        "emit": function (result) {
        }
    });
})

router.post("/terminate_work", function(req, res){
    query.query_insert({
        "addr": "/terminate_work", "call_res": res, "reverse": false, "res_send": true,
        "sql": `UPDATE work_groups SET 
                    work_state = 'terminated', 
                    update_time = '${util.currentDatetime()}'
                    WHERE id = ${req.body.id}`,
        "emit": function (result) {
        }
    });
})

module.exports = router;