# Brooklyn Museum 🎨 Mediachain

## The collection
The Brooklyn Museum has made their entire collection accessible via [REST API available on their website](https://www.brooklynmuseum.org/opencollection/api).

The API exposes a [number of methods](https://www.brooklynmuseum.org/opencollection/api) you can use to explore their entire collection.

For our purposes we're primarily interested in ingesting the following object types:
- Artist
- Object
- Collection
- Exhibition
- Museum Location
- Geographical Locations

## Getting the raw data
Before you begin, you must apply for an api key [via their web form](https://www.brooklynmuseum.org/opencollection/api/register).

Be sure to review their [terms of use](https://www.brooklynmuseum.org/opencollection/api/docs/termsofuse) before starting.

Once you have your API key, clone the repo [NEED LINK]

Find the /config directory in the repo you just cloned and open example_config.py in a text editor.  
Replace [INSERT YOUR API KEY HERE] with your api key and save the file as config.py in the same folder.

Then, in a terminal cd into the main directory of the repo you cloned and run:
```
$ python artist.py
```
This script pings the API and constructs a JSON file called `artists.json` containing all of the artists and their associated metadata in the Brooklyn Museum collection and saves it in the data directory.


## Processing the data
The `artists.json` file consists of one big JSON array, each member of which is an object. We want to turn that into newline-delimited JSON so we can easily generate a schema and publish the data to Mediachain.

Using [jq](https://stedolan.github.io/jq/), we can easily unpack the array: `jq -c '.[]' artists.json > artists.ndjson` - the `.[]` jq filter selects each member of the array and prints it, and the `-c` flag instructs it to use "compact" printing, which results in one object per line.

In your terminal, cd into the data directory and run the following command:
```
$ jq -c '.[]' artists.json > artists.ndjson
```

## Generating a schema
Follow the instructions to install [schema-guru](https://github.com/mediachain/aleph/blob/master/docs/schema-generation.md), a tool that automatically derives a JSON schema from a set of JSON instances. The [schema generation guide](https://github.com/mediachain/aleph/blob/master/docs/schema-generation.md) explains the naming conventions and the parameters we're using:
```
$ schema_guru schema --ndjson --no-length --vendor org.brooklynmuseum --name artist --schemaver 1-0-0 --output org.brooklynmuseum-artist-jsonschema-1-0-0.json artists.ndjson
```

Publish the schema to Mediachain:
```
$ mcclient publishSchema org.brooklynmuseum-artist-jsonschema-1-0-0.json
```

You should see output similar to the following:
```
Published schema with wki = schema:org.brooklynmuseum/artist/jsonschema/1-0-0 to namespace mediachain.schemas
Object ID: QmZZocm4RynNrCe4poQcF7t1pD732dnCqaRFKAwYHwQ2tB
Statement ID: 4XTTM9Y6Sso29BhUFWsNwjRbtmQrTz1oYSPfVNFxMkhLyH7iF:1478808450:0
```

## Publish to Mediachain
We're ready to publish objects from the Brooklyn Museum collection to Mediachain:

```
$ mcclient publish --namespace museums.brooklynmuseum.artist --idFilter .id --schemaReference QmZZocm4RynNrCe4poQcF7t1pD732dnCqaRFKAwYHwQ2tB artist.ndjson
```

## Publishing the rest of the data
Repeat the steps above to create schemas and publish data for objects, collections, exhibitions, museum locations, and geographical locations.

## Interacting with the data
Lets confirm that the data is really in our node!

```
mcclient query "SELECT COUNT(*) FROM museums.brooklynmuseum.*"
```

You can interact with the rest of the data in the same way with MCQL, the Mediachain query language that is very similar to SQL. See the [README](https://github.com/mediachain/concat#basic-operations) for more query examples.

## Going public
See the instructions [here](https://github.com/mediachain/concat#going-public) to configure your NAT, register your node with the directory, and bring it online so anyone can interact with it.

## Conclusion
If you published a new dataset after following this tutorial, reach out to us on [Slack](http://slack.mediachain.io) so we can merge it into the Museum Node with the rest of the museum data!

Open an issue if you have any questions or problems!
