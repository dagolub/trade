import React, { useState, useEffect } from 'react';
import Sidebar from '../../partials/Sidebar';
import Form from '../../components/documents/form';
import Header from '../../partials/Header';
import { getDocument } from '../../services/api';
import { useParams } from 'react-router-dom';
import showError from "../../components/showError";
function UsersEdit() {
  const { id } = useParams();
  const [name, setName] = useState('');
  const [file, setFile] = useState('');
  const [ext, setExt] = useState(false);



  useEffect(() => {
    getDocument(id)
      .then((data) => {
          setName(data.name);
          setFile(data.file);
          setExt(data.ext);
      })
      .catch((error) => {
        showError(error);
      });
  }, [id]);

  return (
    <div className="flex h-[100vh] overflow-hidden">
      <Sidebar />
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
        <Header />
        <main className="grow">
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            <Form
              name={name}
              file={file}
              ext={ext}


              id={id}
            />
          </div>
        </main>
      </div>
    </div>
  );
}

export default UsersEdit;
