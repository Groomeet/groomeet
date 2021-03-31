-- GENERAMOS LOS MUSICOS
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1998-12-29",5);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1995-05-15",6);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1980-09-10",7);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("2000-08-12",8);
INSERT INTO groomeet_backend_musico (fechaNacimiento, usuario_id) VALUES ("1994-09-20",9);

-- A ESOS MUSICOS LOS RELACIONAMOS CON GENEROS
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (4,15);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (5,22);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (6,14);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (7,20);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (4,27);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (5,12);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (6,17);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (7,13);
INSERT INTO groomeet_backend_musico_generos (musico_id, genero_id) VALUES (4,26);

-- A ESOS MUSICOS LOS RELACIONAMOS CON INSTRUMENTOS
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (4,55);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (5,25);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (6,18);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (7,22);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (4,62);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (5,64);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (6,43);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (7,32);
INSERT INTO groomeet_backend_musico_instrumentos (musico_id, instrumento_id) VALUES (4,24);

-- AÑADIMOS LIKES Y NO LIKES ENTRE DICHOS MUSICOS
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (4,6);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (4,7);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (4,8);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (5,4);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (6,5);
INSERT INTO groomeet_backend_musico_likesRecibidos (musico_id,user_id) VALUES (8,4);

INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (8,6);
INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (5,7);
INSERT INTO groomeet_backend_musico_nolikesRecibidos (musico_id,user_id) VALUES (4,3);