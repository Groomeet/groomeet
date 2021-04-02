-- GENERAMOS LOS MUSICOS
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1998-12-29",7);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1995-05-15",8);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1980-09-10",9);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("2000-08-12",10);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1994-09-20",11);

-- A ESOS MUSICOS LOS RELACIONAMOS CON GENEROS
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (1,15);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (2,22);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (3,14);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (4,20);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (5,27);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (1,12);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (2,17);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (3,13);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (1,26);

-- A ESOS MUSICOS LOS RELACIONAMOS CON INSTRUMENTOS
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (1,55);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (2,25);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (3,18);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (4,22);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (5,62);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (1,64);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (2,43);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (1,32);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (2,24);

-- AÑADIMOS LIKES Y NO LIKES ENTRE DICHOS MUSICOS
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (1,8);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (2,9);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (3,10);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (1,9);

INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (5,8);
INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (5,7);
INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (4,7);