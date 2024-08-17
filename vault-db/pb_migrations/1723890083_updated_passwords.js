/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("3zi7iqsx6p1kdy2")

  // remove
  collection.schema.removeField("tkl5xqnx")

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("3zi7iqsx6p1kdy2")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "tkl5xqnx",
    "name": "notes",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
})
