{
   "_id": "_design/all_provider_docs",
   "language": "javascript",
   "views": {
       "by_provider_name": {
           "map": "function(doc) { provider_name = doc._id.split('--').shift(); emit(provider_name, doc._id) }"
       },
       "by_provider_name_and_ingestion_sequence": {
           "map": "function(doc) { provider_name = doc._id.split('--').shift(); emit([provider_name, doc.ingestionSequence], doc._id) }"
       },
       "by_provider_name_count": {
           "map": "function(doc) { provider_name = doc._id.split('--').shift(); emit(provider_name, doc._id) }",
           "reduce": "_count"
       },
       "by_provider_name_and_ingestion_sequence_count": {
           "map": "function(doc) { provider_name = doc._id.split('--').shift(); emit([provider_name, doc.ingestionSequence], doc._id) }",
           "reduce": "_count"
       },
       "by_provider_name_wdoc": {
           "map": "function(doc) { provider_name = doc._id.split('--').shift(); emit(provider_name, doc) }"
       }
   },
    "lists": {
        "lib": {
            "utils": "function getPropByString(obj, propString) {
                if (!propString) return obj;
                var prop, props = propString.split('.');
                var len = props.length;
                for (var i = 0; i < len - 1; i++) {
                    prop = props[i];
                    var candidate = obj[prop];
                    if (candidate !== undefined) {
                        obj = candidate;
                    } else {
                        break;
                    }
                }
                return obj[props[i]];
            }
            exports['getPropByString'] = getPropByString;"
        },
        "has_field_value": "function(head, req) {
            start({'headers': {'Content-Type': 'application/json'}});
            if (!('field' in req.query)) {
                throw new Error('Please supply a field query paramter');
            }
            field = req.query.field;
            value = null;
            if (req.query.value) {
                value = req.query.value;
            }
            send('[');
            first = true;
            var getPropByString = require('lists/lib/utils').getPropByString;
            var row;
            while (row = getRow()) {
                if (!first) {
                    send(',');
                }
                first = false;
                field_obj = getPropByString(row.value, field);
                if (field_obj) {
                    if (value) {
                        if (field_obj !== value) {
                            continue;
                        }
                    }
                    send('{\"'+ row.value._id + '\" : ' + toJSON(field_obj) + '}\\n');
                }
            }
            send(']');
        }",
        "marc_field_value": "function(head, req) {
            /*pymarc records aint the best, better dict by field num*/
            start({'headers': {'Content-Type': 'application/json'}});
            if (!('field' in req.query)) {
                throw new Error('Please supply a field query paramter');
            }
            send('[');
            first = true;
            var row;
            while (row = getRow()) {
                fields =  row.value['originalRecord']['fields'];
                for (idx in fields) {
                    if (fields[idx][req.query.field]) {
                        if (!first) {
                            send(',');
                        }
                        first = false;
                        send('{\"'+ row.value._id + '\" : ' + toJSON(fields[idx]) + '}\\n');
                    }
                }
            }
            send(']');
        }"
    }
}
