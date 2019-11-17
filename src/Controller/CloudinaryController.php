<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;

class CloudinaryController extends AbstractController
{
    /**
     * @Route("/cloudinary", name="cloudinary")
     */
    public function index()
    {
        return $this->render('cloudinary/index.html.twig', [
            'controller_name' => 'CloudinaryController',
        ]);
    }
}
