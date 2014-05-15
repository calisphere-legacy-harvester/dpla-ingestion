{
   "_id": "_design/datesort",
   "language": "javascript",
   "views": {
       "emit-date": {
           "map": "function(doc) { emit(doc.ingestDate, doc._id, doc, 1}"
       }
   }
}
