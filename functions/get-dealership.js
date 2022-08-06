/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */

/**
 * Get all dealerships
 */

const {CloudantV1} = require('@ibm-cloud/cloudant');
const {IamAuthenticator} = require('ibm-cloud-sdk-core');

const COUCH_URL = "https://ce0eb386-bc84-4d6b-9835-df7a265eb4b5-bluemix.cloudantnosqldb.appdomain.cloud";
const IAM_API_KEY = "vjNpEZvoDMXdd77UOly5froHrILEnXICpp_wsynsN92E";


async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({authenticator: authenticator});
    cloudant.setServiceUrl(COUCH_URL);
    
    try {
        const dbName = "dealerships";
        if (params?.state) {
            let found = await cloudant.postFind({db: dbName, selector: {st:{"$eq": params.state}},});
            console.log(found.result)
            return found.result.result;
        } else if (params.state == "" || params.state == null){
            let default_state = await cloudant.postFind({db: dbName, selector:{st: {"$eq": params.st == "CA"}}})
            return default_state.result.result;
        }
        else {
            let db = await cloudant.postAllDocs({db: dbName,includeDocs: true,});
            //let all_dealerships = []
            //db.result.rows.map(function(e) {all_dealerships.push(e.doc);});
            //console.log(all_dealerships);
            //return all_dealerships;
            return {
                    entries:db.result.rows.map((row) => { return {
                              id: row.doc.id,
                              city: row.doc.city,
                              state: row.doc.state,
                              st: row.doc.st,
                              address: row.doc.address,
                              zip: row.doc.zip,
                              lat: row.doc.lat,
                              long: row.doc.long,
                              full_name: row.doc.full_name,
                              short_name: row.doc.short_name
                              
                            }})
                    };
        }      
    } catch (error) {
        return { error: error.description };
    };
}