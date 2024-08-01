import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../css/Dashboard.css';
import Modal from './Modal';



export function handleLogout(navigate) {
  localStorage.clear(); 
  navigate('/');
}

export function handleBack(navigate) {
  navigate(-1);
}


export const LogoutButton = () => {
  const navigate = useNavigate();
  return (
    <button onClick={() => handleLogout(navigate)} className="logout-button"> Logout </button>
  ) 
};

export const BackButton = () => {
  const navigate = useNavigate();
  return (
    <button onClick={() => handleBack(navigate)} className="back-button"> Back </button>
  )
};

export const ChatBox = (props) => {
  const token = props.token;
  const userid = props.userid
  const channelid = props.channelid
  const latest_message = false
  const last_message = 100
  const [text, setText] = useState([]);
  const [names, setNames] = useState(new Map());
  const [message, setMessage] = useState('');
  let id = []

  useEffect(() => {
    fetchChannel();
  }, []);

  useEffect(() => {
    if (text) {
      var objDiv = document.getElementById("chatbox");
      objDiv.scrollTop = objDiv.scrollHeight;
      console.log(text)
      text.map((data) => id.push(data ? data.ownerid : ""))
      id = id.filter(onlyUnique);
      id.map((x) => fetchUser(x));
    }
  }, [text]);

  const fetchChannel = async () => {
    try {
      const response = await fetch(`http://localhost:5001/channel/messages?userid=${userid}&channelid=${channelid}&latest_message=${latest_message}&last_message=${last_message}`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}`},
      });
      const data = await response.json()
      
      setText(data.messages);
      console.log("test")
      

    } catch {}
  };

  const fetchUser = async (userid) => {
    fetch(`http://localhost:5001/user?id=${userid}`, {
      method: 'GET',
      headers: {Authorization: `Bearer ${token}`,},
    })
    .then(res => {
      return res.json();
    })
    .then(data => {
      console.log(data);
      setNames(map => new Map(map.set(userid, data.first_name)))
    })
  };

  const sendMessage = async () => {
    const formdata = new FormData();
    formdata.append('userid', props.userid);
    formdata.append('senderid', props.userid);
    formdata.append('channelid', props.channelid);
    formdata.append('content', message);

    const response = await fetch(`http://localhost:5001/message/send`, {
      method: 'POST',
      body: formdata,
      headers: {
        Authorization: `Bearer ${props.token}`,
      },
    });
    const output = await response.json();
    fetchChannel();
    var objDiv = document.getElementById("chatbox");
    objDiv.scrollTop = objDiv.scrollHeight;
    var objDiv = document.getElementById("box");
    objDiv.value = '';
    // inputRef.current.value = "";
    
  };

  function onlyUnique(value, index, array) {
    return array.indexOf(value) === index;
  }
  
  const listItems = text.toReversed().map((data) => {
    return (<p key={data.content}>{names.get(data.ownerid)}: {data.content}</p>);
  })

  console.log('names', names);
  console.log(listItems);

  return (
    <div>
      <div id="chatbox" style={{textAlign: 'left', maxHeight: '400px', overflow: 'scroll', backgroundColor: '#e2e2e2', padding: '10px'}}>
      {text ? (
        <>
          {listItems}
        </>
      ) : (
        <>
        </>
      )}
      </div>
      <div> 
        <input id='box' type="text" name="Message" onChange={(e) => setMessage(e.target.value)}></input>
        <button onClick={() => sendMessage()}> Send </button>
      </div>
    </div> 
  )
};

export const MessageBox = (props) => {
  const [text, setText] = useState('');

  const sendMessage = async () => {
    try {
      const formdata = new FormData();
      formdata.append('userid', props.userid);
      formdata.append('senderid', props.userid);
      formdata.append('channelid', props.channelid);
      formdata.append('content', text);

      const response = await fetch(`http://localhost:5001/message/send`, {
        method: 'POST',
        body: formdata,
        headers: {
          Authorization: `Bearer ${props.token}`,
        },
      });
      const output = await response.str();
      // inputRef.current.value = "";
      // setText(output);
    }
    catch {
  
    }
  };

  return (
    <div> 
      <input id='text-box' type="text" name="Message" onChange={(e) => setText(e.target.value)}></input>
      <button onClick={() => sendMessage()}> Send </button>
    </div>
  )
};

export const ProjectBox = (props) => {
  const projectid = props.project
  const token = props.token
  const userid = props.userid
  const [project, setProject] = useState([])
  const [skills, setSkills] = useState([])

  useEffect(() => {
    fetchProject()
    fetchSkills()
  }, [])

  const fetchProject = async () => {
    try {
      const resp = await fetch(`http://localhost:5001/project/details?userid=${userid}&projectid=${projectid}`, {
      method: 'GET',
      headers: {Authorization: `Bearer ${token}`,},
    })
      const data = await resp.json()
      console.log(data);
      setProject(data)
    } catch {
      
    }
  };

  const fetchSkills = async () => {
    try {
      const resp = await fetch(`http://localhost:5001/skills/view/project?userid=${userid}&projectid=${projectid}`, {
        method: 'GET',
        headers: {Authorization: `Bearer ${token}`,},
      })
      const data = await resp.json()
      console.log(data);
      setSkills(data)
    } catch {

    }
    
  };

  return (
    <div>
      {projectid ? (
        <>
          <h2> Project: {project.title}</h2>
          
          <h4>Description:</h4>
          <p>{project.additional}</p>
          <h4>Background:</h4>
          <p>{project.background}</p>
          <h4>skills:</h4>
          {Object.values(skills).map((value) => {
            return <p>{value}</p>
          })}
        </>
      ):(
        <>
          <h2>Project: </h2>
          <p>None</p>
        </>
      )}
    </div>
  )
}