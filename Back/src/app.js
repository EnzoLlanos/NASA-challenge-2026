import express from 'express';
import cors from 'cors';

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());

// Ruta de prueba / estado del servidor
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Servidor de Adapting Farms with NASA Data funcionando correctamente'
  });
});

export default app;
