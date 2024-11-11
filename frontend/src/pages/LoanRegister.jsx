import { useState, useEffect } from "react";
import api from "../api"; // Asegúrate de que esta ruta sea correcta
import { useNavigate } from "react-router-dom";

function LoanRegister() {
    const [equipmentList, setEquipmentList] = useState([]);
    const [selectedEquipment, setSelectedEquipment] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Obtener la lista de equipos disponibles
    useEffect(() => {
        const fetchEquipment = async () => {
            try {
                const res = await api.get("/api/v0.1/equipment/"); // Ajusta la ruta según tu API
                setEquipmentList(res.data);
            } catch (error) {
                console.error("Error al obtener equipos:", error);
                setError("Error al cargar equipos");
            }
        };

        fetchEquipment();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const token = localStorage.getItem("ACCESS_TOKEN"); // Asegúrate de que el token esté almacenado
            const userId = localStorage.getItem("USER_ID"); // Asegúrate de que el ID del usuario esté almacenado

            const res = await api.post(
                "/api/v0.1/loans/",
                {
                    user: userId, // ID del usuario autenticado
                    equipment: selectedEquipment, // IDs de los equipos seleccionados
                },
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            console.log("Préstamo registrado:", res.data);
            navigate("/"); // Redirige a la página principal o donde desees
        } catch (error) {
            setError(error.response ? error.response.data : "Error al registrar el préstamo");
            console.error("Error al registrar el préstamo:", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Registrar Préstamo</h1>
            <label htmlFor="equipment">Selecciona el equipo:</label>
            <select
                id="equipment"
                multiple
                value={selectedEquipment}
                onChange={(e) => {
                    const options = e.target.options;
                    const value = [];
                    for (let i = 0; i < options.length; i++) {
                        if (options[i].selected) {
                            value.push(options[i].value);
                        }
                    }
                    setSelectedEquipment(value);
                }}
                required
            >
                {equipmentList.map((item) => (
                    <option key={item.id} value={item.id}>
                        {item.name} {/* Asegúrate de que 'name' sea un campo válido en tu modelo Equipment */}
                    </option>
                ))}
            </select>
            {loading && <p>Cargando...</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
            <button type="submit">Registrar Préstamo</button>
        </form>
    );
}

export default LoanRegister;