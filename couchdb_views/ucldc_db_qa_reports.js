{
    "_id": "_design/qa_reports",
    "views": {
        "lib": {
            "utils": "function value_by_path(obj, path) {
                          var keys = path.split('.');
                          var keyExists = function(obj, keyList) {
                              var cur = keyList.shift();
                              if (cur in obj) {
                                  if (keyList.length <= 0) {
                                      return obj[cur];
                                  } else {
                                      return keyExists(obj[cur], keyList);
                                  }
                              } else if (obj.constructor.toString().indexOf('Array') != -1) {
                                  return obj.map(function(x) { return x[cur]; });
                              } else {
                                  return null;
                              }
                          };
                          if (obj && typeof obj == 'object' && keys.length > 0) {
                              return keyExists(obj, keys);
                          } else {
                              return null;
                          }
                      }
                      function emit_handler(doc, path, date) {
                          if (doc.ingestType != 'item') {
                              return;
                          }
                          var provider = doc._id.split('--').shift();
                          var property = value_by_path(doc, path);
                          if (property) {
                              if (property.constructor.toString().indexOf('Array') == -1) {
                                  property = new Array(property);
                              }
                              for (i = 0; i < property.length; i++) {
                                  if (date) {
                                      emit(
                                           [provider,
                                            property[i].displayDate + ' (' +
                                                property[i].begin + ' to ' +
                                                property[i].end + ')',
                                            doc['_id']
                                           ],
                                           1
                                      );
                                  } else {
                                      emit([provider, property[i], doc['_id']], 1);
                                  }
                              }
                          } else {
                              emit([provider, '__MISSING__', doc['_id']], 1);
                          }
                      }
                      exports['emit_handler'] = emit_handler;
                      function emit_path_value(doc, path, date) {
                          if (doc.ingestType != 'item') {
                              return;
                          }
                          var provider = doc._id.split('--').shift();
                          var property = value_by_path(doc, path);
                          if (property) {
                              if (property.constructor.toString().indexOf('Array') == -1) {
                                  property = new Array(property);
                              }
                              for (i = 0; i < property.length; i++) {
                                  if (date) {
                                      emit(
                                           [
                                            property[i].displayDate + ' (' +
                                                property[i].begin + ' to ' +
                                                property[i].end + ')',
                                            doc['_id']
                                           ],
                                           1
                                      );
                                  } else {
                                      emit([property[i], provider, doc['_id']], 1);
                                  }
                              }
                          } else {
                              emit(['__MISSING__', provider, doc['_id']], 1);
                          }
                      }
                      exports['emit_path_value'] = emit_path_value;"
        },
        "sourceResource.specType": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.specType', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.specType_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.specType', false);
                    }",
            "reduce": "_count"
        },
        "object": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'object', false);
                    }",
            "reduce": "_count"
        },
        "object_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'object', false);
                    }",
            "reduce": "_count"
        },
        "isShownAt": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'isShownAt', false);
                    }",
            "reduce": "_count"
        },
        "isShownAt_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'isShownAt', false);
                    }",
            "reduce": "_count"
        },
        "isShownBy": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'isShownBy', false);
                    }",
            "reduce": "_count"
        },
        "isShownBy_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'isShownBy', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.title": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.title', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.title_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.title', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.creator": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.creator', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.creator_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.creator', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.publisher": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.publisher', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.publisher_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.publisher', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.date": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.date', true);
                    }",
            "reduce": "_count"
        },
        "sourceResource.date_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.date', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.description": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.description', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.description_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.description', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.format": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.format', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.format_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.format', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.type": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.type', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.type_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.type', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.subject.name": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.subject.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.subject.name_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.subject.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.spatial.state": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.spatial.state', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.spatial.state_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.spatial.state', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.spatial.name": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.spatial.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.spatial.name_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.spatial.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.stateLocatedIn.name": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.stateLocatedIn.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.stateLocatedIn.name_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.stateLocatedIn.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.rights": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.rights', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.rights_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.rights', false);
                    }",
            "reduce": "_count"
        },
        "provider.name": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'provider.name', false);
                    }",
            "reduce": "_count"
        },
        "provider.name_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'provider.name', false);
                    }",
            "reduce": "_count"
        },
        "intermediateProvider": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'intermediateProvider', false);
                    }",
            "reduce": "_count"
        },
        "intermediateProvider_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'intermediateProvider', false);
                    }",
            "reduce": "_count"
        },
        "dataProvider": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'dataProvider', false);
                    }",
            "reduce": "_count"
        },
        "dataProvider_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'dataProvider', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.collection.title": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.collection.title', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.collection.title_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.collection.title', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.collection.description": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.collection.description', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.collection.description_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.collection.description', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.contributor": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.contributor', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.contributor_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.contributor', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.language.name": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.language.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.language.name_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.language.name', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.language.iso639_3": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.language.iso639_3', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.language.iso639_3_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.language.iso639_3', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.temporal": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.temporal', true);
                    }",
            "reduce": "_count"
        },
        "sourceResource.temporal_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.temporal', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.isPartOf": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.isPartOf', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.isPartOf_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.isPartOf', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.relation": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.relation', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.relation_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.relation', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.place": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.place', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.place_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.place', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.extent": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.extent', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.extent_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.extent', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.identifier": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'sourceResource.identifier', false);
                    }",
            "reduce": "_count"
        },
        "sourceResource.identifier_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'sourceResource.identifier', false);
                    }",
            "reduce": "_count"
        },
        "validation_invalid_record_messages": {
            "map": "function(doc) {
                        var provider = doc._id.split('--').shift();
                        if (doc.admin !== undefined) {
                            var v = doc.admin.valid_after_enrich;
                            if (v === false) {
                                emit([provider, doc.admin.validation_message, doc['_id']], 1);
                            }
                        }
                    }",
            "reduce": "_count"
        },
        "validation_status": {
            "map": "function(doc) {
                        var provider = doc._id.split('--').shift();
                        var status = 'not validated';
                        if (doc.admin !== undefined) {
                            var v = doc.admin.valid_after_enrich;
                            if (typeof v === 'boolean') {
                                status = (v ? 'valid' : 'invalid');
                            } else {
                                status = 'not validated';
                            }
                        }
                        emit([provider, status, doc['_id']], 1);
                    }",
            "reduce": "_count"
        }
    },
    "lists": {
        "csv": "function(head, req) {
                    start({'headers': {'Content-Type': 'text/csv'}});
                    var row;
                    while (row = getRow()) {
                        send(row.key + ',' + row.value + '\\n');
                    }
                }",
        "count_csv": "function(head, req) {
                          start({'headers': {'Content-Type': 'text/csv'}});
                          var row;
                          while (row = getRow()) {
                              send(row.key + ',' + row.value + '\\n');
                          }
                      }",
        "sort_by_value": "function(head, req) {
                    start({'headers': {'Content-Type': 'application/json'}});
                    var row;
                    var rows=[];
                    while (row = getRow()) {
                        rows.push(row)
                    }
                    /*send(rows[0].key[1]);*/
                    send(toJSON(rows));
                    /*for (index in rows) {
                        row = rows[index];
                        send(toJSON(row)+',\\n');
                    }*/
        }"
    }
}
