{
    "_id": "_design/originalRecord_lookups",
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
        "originalRecord.contributor": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.contributor', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.contributor_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.contributor', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.coverage": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.coverage', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.coverage_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.coverage', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.creator": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.creator', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.creator_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.creator', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.date": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.date', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.date_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.date', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.description": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.description', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.description_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.description', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.format": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.format', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.format_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.format', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.identifier": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.identifier', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.identifier_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.identifier', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.language": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.language', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.language_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.language', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.publisher": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.publisher', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.publisher_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.publisher', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.relation": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.relation', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.relation_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.relation', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.rights": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.rights', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.rights_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.rights', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.source": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.source', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.source_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.source', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.subject": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.subject', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.subject_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.subject', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.title": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.title', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.title_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.title', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.type": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.type', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.type_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.type', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.extent": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.extent', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.extent_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.extent', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.rightsholder": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.rightsholder', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.rightsholder_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.rightsholder', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.temporal": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.temporal', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.temporal_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.temporal', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.alternative": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_handler;
                        emitr(doc, 'originalRecord.alternative', false);
                    }",
            "reduce": "_count"
        },
        "originalRecord.alternative_value": {
            "map": "function(doc) {
                        var emitr = require('views/lib/utils').emit_path_value;
                        emitr(doc, 'originalRecord.alternative', false);
                    }",
            "reduce": "_count"
        }
    }
}
