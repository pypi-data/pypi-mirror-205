import subprocess
from nodejs import node, npm

class InWorldChat:
    """
    A class that allows for communication with the InWorld chat system.

    Attributes:
    inworld_cmd (str): The name of the command to run the InWorld chat system.
    inworld_key (str): The API key for the InWorld chat system.
    inworld_secret (str): The API secret for the InWorld chat system.
    inworld_scene (str): The scene to use for the InWorld chat system.
    """

    def __init__(self, inworld_key, inworld_secret, inworld_scene):
        """
        Initializes a new instance of the InWorldChat class.

        Args:
        inworld_key (str): The API key for the InWorld chat system.
        inworld_secret (str): The API secret for the InWorld chat system.
        inworld_scene (str): The scene to use for the InWorld chat system.
        """
        self.inworld_cmd = "iw.js"
        self.inworld_key = inworld_key
        self.inworld_secret = inworld_secret
        self.inworld_scene = inworld_scene
        
    def setup(self):
        npm.run(['i', '@inworld/nodejs-sdk'])
        npm.run(['i', 'sqlite3'])
        with open('iw.js', 'w') as f:
            f.write("""const{InworldClient:e,InworldPacket:t,ServiceError:a,SessionToken:s,status:r,Session:n}=require("@inworld/nodejs-sdk"),sqlite3=require("sqlite3").verbose(),args=process.argv.slice(2);args.length<7&&(console.error("Usage: node iw.js [INWORLD_KEY] [INWORLD_SECRET] [INWORLD_SCENE] [text] [user_name] [user_channel] [user_id]"),process.exit(1));const INWORLD_KEY=args[0],INWORLD_SECRET=args[1],INWORLD_SCENE=args[2],TEXT=args[3],USER_NAME=args[4],USER_CHANNEL=args[5],USER_ID=args[6],getKey=()=>`${USER_CHANNEL}_${USER_ID}`;class Storage{constructor(e){this.db=new sqlite3.Database(e),this.initializeTable()}async initializeTable(){return new Promise((e,t)=>{this.db.run("CREATE TABLE IF NOT EXISTS data (key TEXT PRIMARY KEY, value TEXT)",a=>{a?t(a):e()})})}get(e){return new Promise((t,a)=>{this.db.get("SELECT value FROM data WHERE key = ?",e,(e,s)=>{e&&a(e),t(s?JSON.parse(s.value):null)})})}set(e,t){return new Promise((a,s)=>{this.db.run("INSERT OR REPLACE INTO data (key, value) VALUES (?, ?)",e,JSON.stringify(t),e=>{e&&s(e),a()})})}delete(e){return new Promise((t,a)=>{this.db.run("DELETE FROM data WHERE key = ?",e,e=>{e&&a(e),t()})})}static async createStorage(e){let t=new Storage(e);return await t.initializeTable(),t}}async function do_inworld_chat(t,a,s,r=0){let n=[],i=getKey(),E=new e().setOnSession({get:async()=>s.get(i),set:e=>s.set(i,e)}).setApiKey({key:INWORLD_KEY,secret:INWORLD_SECRET}).setUser({fullName:a}).setConfiguration({capabilities:{audio:!1,emotions:!1}}).setScene(INWORLD_SCENE).setOnError(async e=>{"1 CANCELLED: Cancelled on client"!==e.message&&(console.error(e),await s.delete(i),r<3?await do_inworld_chat(t,a,s,r+1).catch(console.error):console.error("Maximum retry attempts reached. Operation failed."))}).setOnMessage(e=>{e.isInteractionEnd()?(console.log(n.join(" ")),l.close()):e.isText()&&n.push(e.text.text)}),l=E.build();await l.sendText(t)}Storage.createStorage("data.db").then(e=>{do_inworld_chat(TEXT,USER_NAME,e,0).catch()});""")
        print("File created: iw.js")
        
    def chat(self, query, user_name, user_channel, user_id):
        """
        Sends a message to the InWorld chat system.

        Args:
        query (str): The message to send.
        user_name (str): The name of the user sending the message.
        user_channel (str): The channel to send the message to.
        user_id (str): The ID of the user sending the message.

        Returns:
        str: The output of the chat command, as a string.
        """
        node_process = node.Popen([self.inworld_cmd, 
                    self.inworld_key, 
                    self.inworld_secret,
                    self.inworld_scene,
                    query,
                    user_name,
                    user_channel,
                    user_id],
        stdout=subprocess.PIPE)
        output, error = node_process.communicate()
                                    
        return output.decode('utf-8')
