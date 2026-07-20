import {
  useEffect,
  useState,
  useRef
} from "react";

import ReactMarkdown from "react-markdown";

import {
  Sparkles,
  MessageSquare,
  Send,
  Plus,
  LogOut,
  CircleUserRound
} from "lucide-react";

import "./App.css";


const API_URL =
  "http://127.0.0.1:8000/api/v1";


function App() {


  const [isLoginMode, setIsLoginMode] =
    useState(true);


  const [isAuthenticated, setIsAuthenticated] =
    useState(false);


  const [loading, setLoading] =
    useState(false);


  const [message, setMessage] =
    useState("");


  const [error, setError] =
    useState("");


  const [sessions, setSessions] =
    useState([]);


  const [currentSessionId, setCurrentSessionId] =
    useState(null);


  const [messages, setMessages] =
    useState([]);


  const [isTyping, setIsTyping] =
    useState(false);


  const [userProfile, setUserProfile] =
    useState(null);


  const messagesEndRef =
    useRef(null);


  const [authForm, setAuthForm] =
    useState({

      name: "",

      email: "",

      password: ""

    });


  useEffect(() => {

    const token =
      localStorage.getItem(
        "access_token"
      );


    if (token) {

      setIsAuthenticated(true);

      loadUserProfile();

      loadSessions();

    }

  }, []);


  useEffect(() => {

    messagesEndRef.current?.scrollIntoView({

      behavior: "smooth"

    });

  }, [

    messages,

    isTyping

  ]);


  const getAuthHeaders = () => {

    const token =
      localStorage.getItem(
        "access_token"
      );


    return {

      "Content-Type":
        "application/json",

      "Authorization":
        `Bearer ${token}`

    };

  };


  const loadUserProfile = async () => {

    try {

      const response =
        await fetch(

          `${API_URL}/auth/me`,

          {

            headers:
              getAuthHeaders()

          }

        );


      if (!response.ok) {

        localStorage.removeItem(
          "access_token"
        );

        setIsAuthenticated(false);

        throw new Error(
          "Session expired"
        );

      }


      const data =
        await response.json();


      setUserProfile(data);

    }

    catch (error) {

      console.error(
        error
      );

    }

  };


  const loadSessions = async () => {

    try {

      const response =
        await fetch(

          `${API_URL}/sessions`,

          {

            headers:
              getAuthHeaders()

          }

        );


      if (!response.ok) {

        throw new Error(

          "Failed to load sessions"

        );

      }


      const data =
        await response.json();


      setSessions(data);


      if (

        data.length > 0 &&

        !currentSessionId

      ) {

        loadSessionHistory(

          data[0].session_id

        );

      }

    }

    catch (error) {

      console.error(

        error

      );

    }

  };


  const createNewChat = async () => {

    try {

      const response =
        await fetch(

          `${API_URL}/sessions`,

          {

            method:
              "POST",

            headers:
              getAuthHeaders()

          }

        );


      if (!response.ok) {

        throw new Error(

          "Failed to create session"

        );

      }


      const data =
        await response.json();


      setCurrentSessionId(

        data.session_id

      );


      setMessages([]);


      await loadSessions();

    }

    catch (error) {

      console.error(

        error

      );

    }

  };


  const loadSessionHistory = async (

    sessionId

  ) => {

    try {

      const response =
        await fetch(

          `${API_URL}/sessions/${sessionId}`,

          {

            headers:
              getAuthHeaders()

          }

        );


      if (!response.ok) {

        throw new Error(

          "Failed to load chat history"

        );

      }


      const data =
        await response.json();


      setCurrentSessionId(

        sessionId

      );


      const formattedMessages =
        [];


      data.forEach((chat) => {

        formattedMessages.push({

          id:

            `${chat.timestamp}-user`,

          sender:
            "user",

          text:
            chat.user_message

        });


        formattedMessages.push({

          id:

            `${chat.timestamp}-ai`,

          sender:
            "ai",

          text:
            chat.ai_response

        });

      });


      setMessages(

        formattedMessages

      );

    }

    catch (error) {

      console.error(

        error

      );

    }

  };


  const handleAuthInputChange = (

    event

  ) => {

    const {

      name,

      value

    } = event.target;


    setAuthForm(

      (previousForm) => ({

        ...previousForm,

        [name]:
          value

      })

    );

  };


  const handleAuth = async (

    event

  ) => {

    event.preventDefault();


    setError("");

    setLoading(true);


    try {

      let endpoint = "";

      let requestBody = {};


      if (isLoginMode) {

        endpoint =
          `${API_URL}/auth/login`;


        requestBody = {

          email:
            authForm.email,

          password:
            authForm.password

        };

      }

      else {

        endpoint =
          `${API_URL}/auth/register`;


        requestBody = {

          name:
            authForm.name,

          email:
            authForm.email,

          password:
            authForm.password

        };

      }


      const response =
        await fetch(

          endpoint,

          {

            method:
              "POST",

            headers: {

              "Content-Type":
                "application/json"

            },

            body:
              JSON.stringify(

                requestBody

              )

          }

        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(

          data.detail ||

          "Authentication failed"

        );

      }


      if (isLoginMode) {

        localStorage.setItem(

          "access_token",

          data.access_token

        );


        setIsAuthenticated(

          true

        );


        await loadUserProfile();

        await loadSessions();

      }

      else {

        setIsLoginMode(

          true

        );


        alert(

          "Registration successful! Please login."

        );

      }


      setAuthForm({

        name: "",

        email: "",

        password: ""

      });

    }

    catch (error) {

      setError(

        error.message

      );

    }

    finally {

      setLoading(false);

    }

  };


  const sendMessage = async () => {

    if (

      !message.trim()

    ) {

      return;

    }


    if (

      !currentSessionId

    ) {

      alert(

        "Please create a new chat first."

      );

      return;

    }


    const userMessage =
      message;


    const token =
      localStorage.getItem(

        "access_token"

      );


    setMessages(

      (previousMessages) => [

        ...previousMessages,

        {

          id:
            Date.now(),

          sender:
            "user",

          text:
            userMessage

        }

      ]

    );


    setMessage("");

    setIsTyping(true);


    try {

      const response =
        await fetch(

          `${API_URL}/chat`,

          {

            method:
              "POST",

            headers: {

              "Content-Type":
                "application/json",

              "Authorization":
                `Bearer ${token}`

            },

            body:
              JSON.stringify({

                message:
                  userMessage,

                session_id:
                  currentSessionId

              })

          }

        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(

          data.detail ||

          "Failed to get response"

        );

      }


      setMessages(

        (previousMessages) => [

          ...previousMessages,

          {

            id:
              Date.now() + 1,

            sender:
              "ai",

            text:
              data.reply

          }

        ]

      );


      await loadSessions();

    }

    catch (error) {

      setMessages(

        (previousMessages) => [

          ...previousMessages,

          {

            id:
              Date.now() + 1,

            sender:
              "ai",

            text:

              `Error: ${error.message}`

          }

        ]

      );

    }

    finally {

      setIsTyping(false);

    }

  };


  const handleKeyDown = (

    event

  ) => {

    if (

      event.key === "Enter"

    ) {

      sendMessage();

    }

  };


  const logout = () => {

    localStorage.removeItem(

      "access_token"

    );


    setIsAuthenticated(

      false

    );


    setUserProfile(

      null

    );


    setSessions([]);


    setMessages([]);


    setCurrentSessionId(

      null

    );

  };


  const getUserInitial = () => {

    if (

      !userProfile?.name

    ) {

      return "U";

    }


    return userProfile.name

      .charAt(0)

      .toUpperCase();

  };


  if (

    !isAuthenticated

  ) {

    return (

      <div className="auth-page">

        <div className="auth-card">

          <div className="auth-logo">

            <Sparkles
              size={30}
              strokeWidth={1.8}
            />

          </div>


          <h1>

            AI Customer Support

          </h1>


          <p className="auth-subtitle">

            Multi-Agent AI Support System

          </p>


          <form

            onSubmit={handleAuth}

          >

            {!isLoginMode && (

              <input

                type="text"

                name="name"

                placeholder="Full Name"

                value={

                  authForm.name

                }

                onChange={

                  handleAuthInputChange

                }

                required

              />

            )}


            <input

              type="email"

              name="email"

              placeholder="Email Address"

              value={

                authForm.email

              }

              onChange={

                handleAuthInputChange

              }

              required

            />


            <input

              type="password"

              name="password"

              placeholder="Password"

              value={

                authForm.password

              }

              onChange={

                handleAuthInputChange

              }

              required

            />


            {error && (

              <p className="error-message">

                {error}

              </p>

            )}


            <button

              type="submit"

              className="auth-button"

              disabled={loading}

            >

              {loading

                ? "Please wait..."

                : isLoginMode

                  ? "Login"

                  : "Create Account"}

            </button>

          </form>


          <p className="switch-auth">

            {isLoginMode

              ? "Don't have an account?"

              : "Already have an account?"}


            <button

              onClick={() => {

                setIsLoginMode(

                  !isLoginMode

                );

                setError("");

              }}

            >

              {isLoginMode

                ? "Register"

                : "Login"}

            </button>

          </p>

        </div>

      </div>

    );

  }


  return (

    <div className="app">

      <aside className="sidebar">


        <div className="brand">

          <div className="brand-icon">

            <Sparkles
              size={20}
              strokeWidth={1.8}
            />

          </div>


          <div>

            <h2>

              AI Support

            </h2>


            <p>

              Multi-Agent System

            </p>

          </div>

        </div>


        <button

          className="new-chat-button"

          onClick={createNewChat}

        >

          <Plus
            size={17}
          />

          New Chat

        </button>


        <div className="sidebar-section">

          <p className="section-title">

            Recent Chats

          </p>


          {sessions.length === 0 && (

            <p className="no-chats">

              No chats yet

            </p>

          )}


          {sessions.map((session) => (

            <div

              key={session.session_id}

              className={`chat-item ${

                currentSessionId ===

                session.session_id

                  ? "active"

                  : ""

              }`}

              onClick={() =>

                loadSessionHistory(

                  session.session_id

                )

              }

            >

              <div className="chat-icon">

                <MessageSquare
                  size={15}
                />

              </div>


              <div className="chat-info">

                <p className="chat-title">

                  {session.title}

                </p>


                <small className="chat-last-message">

                  {session.last_message}

                </small>

              </div>

            </div>

          ))}

        </div>


        <div className="sidebar-bottom">


          <div className="user-card">

            <div className="avatar">

              {getUserInitial()}

            </div>


            <div>

              <p>

                {userProfile?.name ||

                  "Loading..."}

              </p>


              <small>

                {userProfile?.email ||

                  "Online"}

              </small>

            </div>

          </div>


          <button

            className="logout-button"

            onClick={logout}

          >

            <LogOut
              size={15}
            />

            Logout

          </button>

        </div>

      </aside>


      <main className="chat-area">


        <header className="chat-header">

          <div>

            <h1>

              Customer Support

            </h1>


            <p>

              Powered by Multi-Agent AI

            </p>

          </div>


          <div className="status">

            <span className="status-dot">

            </span>


            AI Online

          </div>

        </header>


        <section className="messages">


          {messages.length === 0 && (

            <div className="empty-chat">

              <div>

                <Sparkles
                  size={34}
                  strokeWidth={1.5}
                />

              </div>


              <h2>

                How can I help you today?

              </h2>


              <p>

                Ask me about orders, refunds, payments, or technical issues.

              </p>

            </div>

          )}


          {messages.map((chatMessage) => (

            <div

              key={chatMessage.id}

              className={`message-row ${

                chatMessage.sender

              }`}

            >

              <div

                className={`message-avatar ${

                  chatMessage.sender ===

                  "user"

                    ? "user-avatar"

                    : ""

                }`}

              >

                {chatMessage.sender ===

                "ai"

                  ? (

                    <Sparkles
                      size={16}
                      strokeWidth={1.8}
                    />

                  )

                  : getUserInitial()}

              </div>


              <div className="message-bubble">


                {chatMessage.sender ===

                "ai" ? (

                  <ReactMarkdown>

                    {chatMessage.text}

                  </ReactMarkdown>

                ) : (

                  <p>

                    {chatMessage.text}

                  </p>

                )}

              </div>

            </div>

          ))}


          {isTyping && (

            <div className="message-row ai">

              <div className="message-avatar">

                <Sparkles
                  size={16}
                  strokeWidth={1.8}
                />

              </div>


              <div className="loading-message">

                <span className="loading-dot">

                </span>


                <span className="loading-dot">

                </span>


                <span className="loading-dot">

                </span>

              </div>

            </div>

          )}


          <div ref={messagesEndRef} />

        </section>


        <div className="input-area">


          <div className="input-container">

            <input

              type="text"

              placeholder="Ask anything about your order, payment, refund..."

              value={message}

              onChange={(event) =>

                setMessage(

                  event.target.value

                )

              }

              onKeyDown={handleKeyDown}

            />


            <button

              className="send-button"

              onClick={sendMessage}

            >

              <Send
                size={17}
              />

            </button>

          </div>


          <p className="input-hint">

            AI Support can make mistakes. Please verify important information.

          </p>

        </div>

      </main>

    </div>

  );

}


export default App;